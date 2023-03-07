import pygame
from typing import Union, Sequence
from timer import Timer
import logging
from utils import AttackType


class KingBibleGenerator(pygame.sprite.Group):
    def __init__(self, groups: Union[Sequence[pygame.sprite.Group], pygame.sprite.Group], proj_count: int):
        super().__init__()
        self.groups = groups
        self.proj_count = proj_count
        self.initial_angles = self.calc_inital_angles(proj_count=self.proj_count)
        self.rotation_speed = 150
        self.radius = 150
        self.lifetime = Timer(3000, self.kill_all_sprites)
        self.cooldown = Timer(3000)

        self.logger = logging.getLogger('kingbiblegenerator')

        self.projectile_image = pygame.image.load('./assets/animation_frames/attacks/king_bible/moving/Screenshot_2023-03-06_185039-removebg-preview.png')
        self.projectile_image = pygame.transform.scale_by(self.projectile_image, 0.15)

    @staticmethod
    def calc_inital_angles(proj_count: int) -> list[int]:
        region_size = 360 // proj_count
        return [0 + region_size * i for i in range(proj_count)]

    def kill_all_sprites(self):
        for sprite in self.sprites():
            sprite.kill()
        self.cooldown.activate()
        self.logger.debug('Destroying existing sprites')

    def create_sprites(self, player_pos):
        for angle in self.initial_angles:
            KingBibleProjectile(groups=(self, self.groups), initial_angle=angle, player_pos=player_pos, radius=self.radius, image=self.projectile_image, rotation_speed=self.rotation_speed)
        self.lifetime.activate()

    def update_sprites(self, dt, player_pos):
        for sprite in self.sprites():
            sprite.update_bible_projectile(dt, player_pos)

    def update(self, dt, player_pos: tuple):
        if self.lifetime.active:
            self.lifetime.update()
        if len(self.sprites()) > 0:  # Update the angle of the existing sprites
            self.update_sprites(dt, player_pos)
        else:  # Create new sprites
            if not self.cooldown.active:
                self.logger.debug('Creating new sprites')
                self.create_sprites(player_pos)
            else:
                self.cooldown.update()


class KingBibleProjectile(pygame.sprite.Sprite):
    def __init__(self, groups, initial_angle, player_pos, image, radius, rotation_speed):
        super().__init__(groups)

        self.attack_type = AttackType.KING_BIBLE

        self.image = image

        self.initial_angle = initial_angle
        self.angle = self.initial_angle
        self.rotation_speed = rotation_speed
        self.radius = radius

        self.pos = self.set_pos(self.radius, self.angle, player_pos)
        self.rect = self.image.get_rect(center=self.pos)

    @staticmethod
    def set_pos(radius, angle, player_pos):
        pos = pygame.math.Vector2()
        pos.from_polar((radius, angle))
        pos += pygame.math.Vector2(player_pos)
        return pos

    def update_bible_projectile(self, dt, player_pos):
        self.angle += self.rotation_speed * dt
        self.angle %= 360

        self.pos = self.set_pos(self.radius, self.angle, player_pos)
        self.rect = self.image.get_rect(center=self.pos)
