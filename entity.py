from math import atan2, degrees, pi
from typing import Union

import pygame

from utils import Status


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups: list[pygame.sprite.Group], pos: tuple[int, int], status: Union[Status, str]) -> None:
        super().__init__(groups)

        self.animation_frames = self.import_frames()
        self.animation_speed = 5
        self.frame_index = 0

        self.status = status
        self.image = self.get_animation_frame_by_index(self.frame_index)

        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(self.rect.center)

        self.direction = pygame.math.Vector2(0, 0)
        self.movement_speed = 0

    def import_frames(self) -> dict[str: list[pygame.Surface]]:
        return {}

    @staticmethod
    def calculate_angle_between_vectors(v1: pygame.math.Vector2, v2: pygame.math.Vector2) -> float:
        dx = v1.x - v2.x
        dy = v1.y - v2.y

        rads = atan2(-dy, dx)
        rads %= 2 * pi
        degs = degrees(rads)
        return degs

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(self.animation_frames[str(self.status)]):
            self.frame_index = 0
        self.image = self.get_animation_frame_by_index(int(self.frame_index))

    def move(self, dt):
        self.pos += (self.direction * self.movement_speed * dt)
        self.rect.center = self.pos

    def get_animation_frame_by_index(self, index: int) -> pygame.Surface:
        return self.animation_frames[str(self.status)][index]
