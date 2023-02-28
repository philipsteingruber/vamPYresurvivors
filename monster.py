import random

import pygame

from entity import Entity
from utils import import_images_from_folder
from timer import Timer
from typing import Callable
import random


class Monster(Entity):
    def __init__(self, groups: list[pygame.sprite.Group], pos: tuple[int, int], monster_type: str, increase_xp: Callable) -> None:
        self.monster_type = monster_type
        super().__init__(groups, pos, 'idle')
        self.turned = Timer(200)
        self.invulnerable = Timer(100)
        self.increase_xp = increase_xp

        self.animation_speed = round(random.triangular(4.5, 5.5), 2)

        if self.monster_type == 'slime':
            self.movement_speed = 100
            self.rect = self.rect.inflate(-40, -40)
            self.health = random.randint(1, 5)
            self.xp_value = 5

    def import_frames(self) -> dict[str: list[pygame.Surface]]:
        animations = {'idle': [], 'walk': []}
        base_path = f'assets/animation_frames/monsters/{self.monster_type}/'

        # Idle frames
        idle_path = base_path + 'idle/'
        animations['idle'] = import_images_from_folder(path=idle_path, scale_factor=2, flip=False)

        # Walking frames
        walking_path = base_path + random.choice(['walk1', 'walk2']) + '/'
        animations['walk'] = import_images_from_folder(path=walking_path, scale_factor=2, flip=False)

        return animations

    def get_player_direction_normalized(self, player_pos: tuple[int, int]) -> pygame.math.Vector2:
        monster_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player_pos)

        result_vec = player_vec - monster_vec
        if result_vec.magnitude() > 0:
            result_vec = result_vec.normalize()
        return result_vec

    @property
    def damageable(self) -> bool:
        return not self.invulnerable.active

    def check_death(self) -> None:
        if self.health <= 0:
            self.increase_xp(self.xp_value)
            self.kill()

    def get_player_direction(self, player_pos: tuple[int, int]) -> pygame.math.Vector2:
        monster_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player_pos)

        return player_vec - monster_vec

    def get_player_distance(self, player_pos: tuple[int, int]) -> float:
        monster_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player_pos)

        result_vec = player_vec - monster_vec
        return result_vec.magnitude()

    def update_direction(self, player_pos: tuple[int, int]) -> None:
        if self.direction.magnitude() > 1:
            current_dir = self.direction.as_polar()
            player_dir = self.get_player_direction_normalized(player_pos).as_polar()
            mid = (current_dir[1] + player_dir[1]) / 2
            self.direction = self.direction.rotate(mid - current_dir[1])
        else:
            self.direction = self.get_player_direction_normalized(player_pos)

    def update_monster(self, player_pos: tuple[int, int], dt: float) -> None:
        if not self.turned.active:
            self.update_direction(player_pos)
            self.turned.activate()
        else:
            self.turned.update()
        self.move(dt)

    def update(self, dt: float) -> None:
        self.invulnerable.update()
        self.animate(dt)
