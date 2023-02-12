import random

import pygame

from entity import Entity
from utils import import_images_from_folder


class Monster(Entity):
    def __init__(self, groups: list[pygame.sprite.Group], pos: tuple[int, int], monster_type: str):
        self.monster_type = monster_type
        super().__init__(groups, pos, 'idle')
        self.movement_speed = 100
        self.rect = self.rect.inflate(-40, -40)

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

    def get_player_direction(self, player_pos: tuple[int, int]) -> pygame.math.Vector2:
        monster_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player_pos)

        return player_vec - monster_vec

    def get_player_distance(self, player_pos: tuple[int, int]):
        monster_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player_pos)

        result_vec = player_vec - monster_vec
        return result_vec.magnitude()

    def update_monster(self, player_pos: tuple[int, int], dt):
        if self.direction.magnitude() > 0:
            current_dir = self.direction.as_polar()
            player_dir = self.get_player_direction_normalized(player_pos).as_polar()
            mid = (current_dir[1] + player_dir[1]) / 2
            self.direction = self.direction.rotate(mid - current_dir[1])
        else:
            self.direction = self.get_player_direction_normalized(player_pos)

        self.move(dt)

    def update(self, dt) -> None:
        self.animate(dt)
