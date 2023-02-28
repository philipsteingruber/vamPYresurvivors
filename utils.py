import os
from dataclasses import dataclass
from enum import Enum

import pygame
from pygame.math import Vector2


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


def vector_between_sprites(sprite_a, sprite_b) -> Vector2:
    vec_a = Vector2(sprite_a.pos)
    vec_b = Vector2(sprite_b.pos)
    return vec_a - vec_b


@dataclass
class Status:
    direction: str
    action: str

    def __str__(self) -> str:
        return f'{self.direction}_{self.action}'

    def __repr__(self) -> str:
        return f'{self.direction}_{self.action}'


class AttackType(Enum):
    MAGIC_WAND = 'magic_wand'
    KING_BIBLE = 'bible'


class LevelUpType(Enum):
    PROJECTILE_COUNT = 'projectile_count'
    COOLDOWN_MOD = 'cooldown_mod'
    FLAT_DAMAGE_MOD = 'flat_damage_mod'
    PIERCE_COUNT = 'pierce_count'
