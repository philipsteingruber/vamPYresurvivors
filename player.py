from typing import Callable

import pygame

from entity import Entity
from settings import LEVEL_UP_DATA
from timer import Timer
from utils import import_images_from_folder, Status, AttackType, LevelUpType


class Player(Entity):
    def __init__(self, pos: tuple[int, int], groups: list[pygame.sprite.Group], create_attack: Callable) -> None:
        super().__init__(groups, pos, Status(direction='down', action='idle'))

        self.movement_speed = 250
        self.create_attack = create_attack
        self.attack_timers = {AttackType.MAGIC_WAND: Timer(duration=1200)}
        for timer in self.attack_timers.values():
            timer.activate()

        self.projectile_counts = {AttackType.MAGIC_WAND: 2}
        self.pierce_counts = {AttackType.MAGIC_WAND: 0}
        self.weapon_levels = {AttackType.MAGIC_WAND: 1}
        self.flat_damage_mods = {AttackType.MAGIC_WAND: 0}

        self.xp = 0
        self.total_level = 1
        self.next_level_up = 5

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

    def level_up_weapon(self, attack_type: AttackType) -> None:
        self.weapon_levels[attack_type] += 1
        if self.weapon_levels[attack_type] > 8:
            self.weapon_levels[attack_type] = 8
        else:
            self.total_level += 1
            self.increase_xp_required_for_level_up()

            level_up_type, value = LEVEL_UP_DATA[attack_type][self.weapon_levels[attack_type]]
            if level_up_type == LevelUpType.PROJECTILE_COUNT:
                self.projectile_counts[attack_type] += 1
            elif level_up_type == LevelUpType.COOLDOWN_MOD:
                old_timer_duration = self.attack_timers[attack_type].duration
                self.attack_timers[attack_type] = Timer(old_timer_duration - value)
                self.attack_timers[attack_type].activate()
            elif level_up_type == LevelUpType.FLAT_DAMAGE_MOD:
                self.flat_damage_mods[attack_type] += value
            elif level_up_type == LevelUpType.PIERCE_COUNT:
                self.pierce_counts[attack_type] += value

    def print_weapon_data(self, attack_type):
        print('Current level:', self.weapon_levels[attack_type],
              'Proj count:', self.projectile_counts[attack_type],
              'Pierce count.', self.pierce_counts[attack_type],
              'Damage mod:', self.flat_damage_mods[attack_type],
              'Cooldown:', self.attack_timers[attack_type].duration)

    def increase_xp_required_for_level_up(self) -> None:
        if self.total_level <= 20:
            self.next_level_up += 10
        elif self.total_level <= 40:
            self.next_level_up += 13
        else:
            self.next_level_up += 16

        if self.total_level == 20:
            self.next_level_up += 600
        elif self.total_level == 40:
            self.next_level_up += 2400

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
        if direction != self.status.direction:
            self.frame_index = 0
        if direction:
            self.status.direction = direction

    def update(self, dt: float) -> None:
        self.direction = self.get_direction_normalized()
        self.move(dt)
        self.set_status()
        self.animate(dt)

        if self.xp >= self.next_level_up:
            self.level_up_weapon(AttackType.MAGIC_WAND)

        for timer in self.attack_timers.values():
            timer.update()
        for attack_type, timer in self.attack_timers.items():
            if not timer.active:
                self.create_attack(attack_type)
                timer.activate()
