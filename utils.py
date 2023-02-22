import os

import pygame
from pygame.math import Vector2
from entity import Entity


def import_images_from_folder(path: str, scale_factor: float = 1, flip: bool = False) -> list[pygame.Surface]:
    surface_list = []

    for _, __, image_files in os.walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image = pygame.image.load(full_path).convert_alpha()

            image = pygame.transform.scale_by(image, scale_factor)
            if flip:
                image = pygame.transform.flip(image, flip_x=True, flip_y=False)

            surface_list.append(image)

    return surface_list


def vector_between_sprites(sprite_a: Entity, sprite_b: Entity) -> Vector2:
    vec_a = Vector2(sprite_a.pos)
    vec_b = Vector2(sprite_b.pos)
    return vec_a - vec_b


class Status:
    def __init__(self, direction: str, action: str) -> None:
        self.direction = direction
        self.action = action

    def __str__(self) -> str:
        return f'{self.direction}_{self.action}'

    def __repr__(self) -> str:
        return f'{self.direction}_{self.action}'

