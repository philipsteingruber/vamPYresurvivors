import pygame

from entity import Entity
from utils import import_images_from_folder, Status
from typing import Callable
from timer import Timer
from collections import defaultdict


class Player(Entity):
    def __init__(self, pos: tuple[int, int], groups: list[pygame.sprite.Group], create_attack: Callable) -> None:
        super().__init__(groups, pos, Status(direction='down', action='idle'))

        self.movement_speed = 250
        self.create_attack = create_attack
        self.attack_timers = {'magic_wand': Timer(duration=2000)}
        for timer in self.attack_timers.values():
            timer.activate()

        self.projectile_counts = {'magic_wand': 2}
        self.weapon_levels = defaultdict(int)
        self.xp = 0
        self.next_level_up = 50

    def import_frames(self) -> dict[str: list[pygame.Surface]]:
        animations = {'down_idle': [], 'left_idle': [], 'right_idle': [], 'up_idle': [], 'down_walk': [], 'left_walk': [], 'right_walk': [], 'up_walk': []}
        base_path = 'assets/animation_frames/player/'
        for animation in animations:
            if animation.startswith('left'):
                temp_animation = animation.replace('left', 'right')
                full_path = base_path + temp_animation + '/'
                animations[animation] = import_images_from_folder(path=full_path, scale_factor=2.5, flip=True)
            else:
                full_path = base_path + animation + '/'
                animations[animation] = import_images_from_folder(path=full_path, scale_factor=2.5, flip=False)
        return animations

    @staticmethod
    def get_direction_normalized() -> pygame.math.Vector2:
        keys = pygame.key.get_pressed()

        direction = pygame.math.Vector2(0, 0)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            direction.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            direction.y = 1
        else:
            direction.y = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction.x = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction.x = 1
        else:
            direction.x = 0

        if direction.magnitude() > 0:
            direction = direction.normalize()

        return direction

    def level_up_weapon(self, weapon_name: str) -> None:
        self.weapon_levels[weapon_name] += 1
        if self.weapon_levels[weapon_name] > 8:
            self.weapon_levels[weapon_name] = 8
        else:
            self.next_level_up *= 3
            if weapon_name == 'magic_wand':
                self.projectile_counts[weapon_name] += 1

    def set_status(self) -> None:
        if self.direction.magnitude() == 0:
            action = 'idle'
        else:
            action = 'walk'
        if action != self.status.action:
            self.frame_index = 0
        self.status.action = action

        direction = None
        if self.direction.y == -1:
            direction = 'up'
        elif self.direction.y == 1:
            direction = 'down'
        if self.direction.x == 1:
            direction = 'right'
        elif self.direction.x == -1:
            direction = 'left'
        if direction:
            if direction != self.status.direction:
                self.frame_index = 0
            self.status.direction = direction

    def update(self, dt: float) -> None:
        self.direction = self.get_direction_normalized()
        self.move(dt)
        self.set_status()
        self.animate(dt)

        if self.xp >= self.next_level_up:
            self.level_up_weapon('magic_wand')

        for timer in self.attack_timers.values():
            timer.update()
        for attack_type, timer in self.attack_timers.items():
            if not timer.active:
                self.create_attack(attack_type)
                timer.activate()
