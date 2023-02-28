from typing import Sequence, Union

import pygame

from entity import Entity
from timer import Timer
from utils import import_images_from_folder, AttackType


class Attack(Entity):
    def __init__(self, pos: tuple[int, int], direction: pygame.math.Vector2, attack_type: AttackType, groups: Union[Sequence[pygame.sprite.Group], pygame.sprite.Group], pierce_count: int, damage_mod=0) -> None:
        self.attack_type = attack_type
        super().__init__(groups, pos, 'moving')

        if self.attack_type == AttackType.MAGIC_WAND:
            self.direction = direction
            self.lifetime = Timer(duration=5000, func=self.kill)
            self.lifetime.activate()
            self.movement_speed = 150
            self.damage = 20 + damage_mod
            self.pierce_count = pierce_count

    def import_frames(self) -> dict[str: list[pygame.Surface]]:
        return {'moving': import_images_from_folder(f'./assets/animation_frames/attacks/{self.attack_type.value}/moving/', scale_factor=0.5)}

    def update(self, dt) -> None:
        self.lifetime.update()
        self.animate(dt)
        self.move(dt)
