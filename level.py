import random

import pygame

from debug import debug
from monster import Monster
from player import Player
from entity import Entity
from attack import Attack
from pygame.math import Vector2
from typing import Union


class Level:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()

        self.all_sprites = CameraGroup()
        self.monster_sprites: pygame.sprite.Group[Monster] = pygame.sprite.Group()
        self.attack_sprites: pygame.sprite.Group[Attack] = pygame.sprite.Group()

        self.player = Player(pos=(750, 500), groups=[self.all_sprites], create_attack=self.create_attack)

        for _ in range(5):
            Monster(groups=[self.all_sprites, self.monster_sprites], pos=(random.randint(-500, 1500), random.randint(-500, 1500)), monster_type='slime')

    def create_monster_quadrants(self) -> list[pygame.sprite.Group]:
        nw_monsters = []
        ne_monsters = []
        se_monsters = []
        sw_monsters = []

        player_pos = self.player.rect.center
        for monster in self.monster_sprites:
            if not (monster.get_player_distance(player_pos) > (self.display_surface.get_width() / 2) + 100):
                player_dir: pygame.math.Vector2 = monster.get_player_direction_normalized(player_pos)
                if player_dir.x >= 0 and player_dir.y >= 0:
                    se_monsters.append(monster)
                elif player_dir.x >= 0 and player_dir.y <= 0:
                    ne_monsters.append(monster)
                elif player_dir.x <= 0 and player_dir.y >= 0:
                    sw_monsters.append(monster)
                elif player_dir.x <= 0 and player_dir.y <= 0:
                    nw_monsters.append(monster)

        return [pygame.sprite.Group(nw_monsters), pygame.sprite.Group(ne_monsters), pygame.sprite.Group(se_monsters), pygame.sprite.Group(sw_monsters)]

    def check_attack_collisions(self) -> None:
        colliding_attacks: dict[Monster: Attack] = pygame.sprite.groupcollide(self.monster_sprites, self.attack_sprites, dokilla=False, dokillb=False)
        if colliding_attacks:
            for monster, attacklist in colliding_attacks.items():
                for attack in attacklist:
                    if attack.attack_type == 'magic_wand':
                        monster.health -= attack.damage
                        attack.kill()
                        monster.check_death()

    @staticmethod
    def check_monster_collisions(monster_quadrants: list[pygame.sprite.Group]) -> None:
        sprite_radius = 14
        for quadrant in monster_quadrants:
            for monster in quadrant:
                other_monster: Monster
                for other_monster in quadrant:
                    if monster is other_monster:
                        continue
                    collision_vector = pygame.math.Vector2(monster.pos - other_monster.pos) * 0.5
                    if collision_vector.magnitude() < sprite_radius:
                        collision_vector = collision_vector.normalize() * (abs(sprite_radius-collision_vector.magnitude()))
                        monster.pos += collision_vector
                        monster.rect.center = monster.pos
                        other_monster.pos -= collision_vector
                        other_monster.rect.center = other_monster.pos

    def create_attack(self, attack_type: str) -> None:
        monster_sprites_by_distance = self.monster_sprites_sorted_by_distance()
        if attack_type == 'magic_wand':
            nearest_monster: Monster = monster_sprites_by_distance[0]
            Attack(pos=self.player.rect.center, direction=self.vector_between_sprites(nearest_monster, self.player).normalize(), attack_type=attack_type, groups=[self.attack_sprites, self.all_sprites])

    def monster_distance_to_player(self, monster: Monster):
        return self.vector_between_sprites(self.player, monster).magnitude()

    def monster_sprites_sorted_by_distance(self) -> list[Monster]:
        return sorted(self.monster_sprites.sprites(), key=self.monster_distance_to_player)

    @staticmethod
    def vector_between_sprites(sprite_a: Entity, sprite_b: Entity) -> Vector2:
        vec_a = Vector2(sprite_a.pos)
        vec_b = Vector2(sprite_b.pos)
        return vec_a - vec_b

    def run(self, dt: float) -> None:
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.player)

        for monster in self.monster_sprites:
            monster.update_monster(player_pos=self.player.rect.center, dt=dt)

        # Start using quadrants if we get performance issues
        # self.check_monster_collisions(self.create_monster_quadrants())
        self.check_monster_collisions([self.monster_sprites])
        self.check_attack_collisions()

        if dt > 0:
            debug(round(1/dt))


class CameraGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()

        self.display_surface = pygame.display.get_surface()

        # Camera attributes
        self.half_width = self.display_surface.get_width() // 2
        self.half_height = self.display_surface.get_height() // 2
        self.offset = pygame.math.Vector2(0, 0)

        # Floor attributes
        self.floor_surface = pygame.image.load('assets/map/map.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def set_offset(self, player: Player) -> None:
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

    def draw_floor(self) -> None:
        offset_rect = self.floor_rect.copy()
        offset_rect.center -= self.offset
        self.display_surface.blit(self.floor_surface, offset_rect)

    def draw_sprites(self) -> None:
        sprite: Entity
        for sprite in self.sprites():
            offset_rect = sprite.rect.copy()
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)

    def draw(self, player: Player) -> None:
        self.set_offset(player)
        self.draw_floor()
        self.draw_sprites()
