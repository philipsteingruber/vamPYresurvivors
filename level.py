import pygame
from player import Player


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.all_sprites = CameraGroup()

        self.player = Player((150, 50), [self.all_sprites, self.all_sprites])

    def run(self, dt):
        self.all_sprites.update(dt)
        self.all_sprites.calculate_offset(self.player)
        self.all_sprites.draw_floor()
        self.all_sprites.draw_sprites()


class CameraGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()

        self.display_surface = pygame.display.get_surface()

        # Camera attributes
        self.half_width = self.display_surface.get_width() // 2
        self.half_height = self.display_surface.get_height() // 2
        self.offset = pygame.math.Vector2(0, 0)

        # Floor attributes
        self.floor_surface = pygame.image.load('./map/map.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def calculate_offset(self, player: Player) -> tuple[int, int]:
        offset_x = player.rect.centerx - self.half_width
        offset_y = player.rect.centery - self.half_height
        self.offset.x, self.offset.y = offset_x, offset_y

    def draw_floor(self) -> None:
        offset_rect = self.floor_rect.copy()
        offset_rect.center -= self.offset
        self.display_surface.blit(self.floor_surface, offset_rect)

    def draw_sprites(self):
        print(self.offset)
        for sprite in self.sprites():
            offset_rect = sprite.rect.copy()
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)
