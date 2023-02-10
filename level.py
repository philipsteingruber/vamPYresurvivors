import random

import pygame

from monster import Monster
from player import Player
from settings import MONSTER_SIZE
from debug import debug


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.all_sprites = CameraGroup()
        self.monster_sprites: pygame.sprite.Group[Monster] = pygame.sprite.Group()

        self.player = Player((750, 500), [self.all_sprites])

        for _ in range(2):
            Monster(groups=[self.all_sprites, self.monster_sprites], pos=(random.randint(500, 1000), random.randint(500, 1000)), monster_type='slime')

    def create_monster_quadrants(self) -> list[list[Monster]]:
        nw_monsters = []
        ne_monsters = []
        se_monsters = []
        sw_monsters = []

        player_pos = self.player.rect.center
        for monster in self.monster_sprites:
            if not (monster.get_player_distance(player_pos) > (self.display_surface.get_width() / 2) + 100):
                player_dir: pygame.math.Vector2 = monster.get_player_direction(player_pos)
                if player_dir.x > 0 and player_dir.y > 0:
                    se_monsters.append(monster)
                elif player_dir.x > 0 and player_dir.y < 0:
                    ne_monsters.append(monster)
                elif player_dir.x < 0 and player_dir.y > 0:
                    sw_monsters.append(monster)
                elif player_dir.x < 0 and player_dir.y < 0:
                    nw_monsters.append(monster)

        return [nw_monsters, ne_monsters, se_monsters, sw_monsters]

    @staticmethod
    def check_monster_collisions(monster_quadrants: list[list[Monster]]):
        allowed_overlap = MONSTER_SIZE // 3
        for quadrant_monsters in monster_quadrants:
            for monster in quadrant_monsters:
                for other_monster in quadrant_monsters:
                    if monster.pos != other_monster.pos and not monster.collided.active and not other_monster.collided.active:
                        old_pos = monster.pos
                        if monster.pos.y - other_monster.pos.y < allowed_overlap:
                            if monster.pos.y < other_monster.pos.y:
                                monster.pos.y -= allowed_overlap
                            else:
                                monster.pos.y += allowed_overlap
                        if monster.pos.x - other_monster.pos.y < allowed_overlap:
                            if monster.pos.x < other_monster.pos.x:
                                monster.pos.x -= allowed_overlap
                            else:
                                monster.pos.x += allowed_overlap
                        if monster.pos != old_pos:
                            print('moved')
                            monster.rect.center = monster.pos
                            monster.collided.activate()
                            other_monster.collided.activate()

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

        self.check_monster_collisions(self.create_monster_quadrants())

        if dt > 0:
            debug(1/dt)

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
