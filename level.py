import random

import pygame

from debug import debug
from monster import Monster
from player import Player
from settings import MONSTER_SIZE


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.all_sprites = CameraGroup()
        self.monster_sprites: pygame.sprite.Group[Monster] = pygame.sprite.Group()

        self.player = Player((750, 500), [self.all_sprites])

        for _ in range(200):
            Monster(groups=[self.all_sprites, self.monster_sprites], pos=(random.randint(500, 1000), random.randint(500, 1000)), monster_type='slime')

    def create_monster_quadrants(self) -> list[pygame.sprite.Group]:
        nw_monsters = []
        ne_monsters = []
        se_monsters = []
        sw_monsters = []

        player_pos = self.player.rect.center
        for monster in self.monster_sprites:
            if not (monster.get_player_distance(player_pos) > (self.display_surface.get_width() / 2) + 100):
                player_dir: pygame.math.Vector2 = monster.get_player_direction(player_pos)
                if player_dir.x >= 0 and player_dir.y >= 0:
                    se_monsters.append(monster)
                elif player_dir.x >= 0 and player_dir.y <= 0:
                    ne_monsters.append(monster)
                elif player_dir.x <= 0 and player_dir.y >= 0:
                    sw_monsters.append(monster)
                elif player_dir.x <= 0 and player_dir.y <= 0:
                    nw_monsters.append(monster)

        return [pygame.sprite.Group(nw_monsters), pygame.sprite.Group(ne_monsters), pygame.sprite.Group(se_monsters), pygame.sprite.Group(sw_monsters)]

    @staticmethod
    def check_monster_collisions(monster_quadrants: list[pygame.sprite.Group]):
        sprite_radius = 14
        for quadrant in monster_quadrants:
            for monster in quadrant:
                other_monster: Monster
                for other_monster in quadrant:
                    if other_monster is not monster:
                        collision_vector = pygame.math.Vector2(monster.pos - other_monster.pos) * 0.5
                        if collision_vector.magnitude() < sprite_radius:
                            collision_vector = collision_vector.normalize() * (abs(sprite_radius-collision_vector.magnitude()))
                            monster.pos += collision_vector
                            monster.rect.center = monster.pos
                            other_monster.pos -= collision_vector
                            other_monster.rect.center = other_monster.pos

    @staticmethod
    def get_monster_distance(monster_x: Monster, monster_y: Monster) -> float:
        return (pygame.math.Vector2(monster_x.rect.center) - pygame.math.Vector2(monster_y.rect.center)).magnitude()

    def run(self, dt):
        self.all_sprites.update(dt)
        self.all_sprites.set_offset(self.player)
        self.all_sprites.draw_floor()
        self.all_sprites.draw_sprites()

        for monster in self.monster_sprites:
            monster.update_monster(player_pos=self.player.rect.center, dt=dt)

        # self.check_monster_collisions(self.create_monster_quadrants())
        self.check_monster_collisions([self.monster_sprites])



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
        offset_x = player.rect.centerx - self.half_width
        offset_y = player.rect.centery - self.half_height
        self.offset.x, self.offset.y = offset_x, offset_y

    def draw_floor(self) -> None:
        offset_rect = self.floor_rect.copy()
        offset_rect.center -= self.offset
        self.display_surface.blit(self.floor_surface, offset_rect)

    def draw_sprites(self):
        for sprite in self.sprites():
            offset_rect = sprite.rect.copy()
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)
