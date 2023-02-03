import pygame
from player import Player
from monster import Monster
import random


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.all_sprites = CameraGroup()
        self.monster_sprites: pygame.sprite.Group[Monster] = pygame.sprite.Group()

        self.player = Player((750, 500), [self.all_sprites])

        for _ in range(25):
            Monster(groups=[self.all_sprites, self.monster_sprites], pos=(random.randint(500, 1000), random.randint(500, 1000)), monster_type='slime')

    def run(self, dt):
        self.all_sprites.update(dt)
        self.all_sprites.set_offset(self.player)
        self.all_sprites.draw_floor()
        self.all_sprites.draw_sprites()

        for monster in self.monster_sprites:
            monster.update_monster(self.player.rect.center, dt)


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
