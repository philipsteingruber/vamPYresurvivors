import pygame
from typing import Sequence, Union
from entity import Entity
from timer import Timer
from utils import import_images_from_folder


class Attack(Entity):
    def __init__(self, pos: tuple[int, int], direction: pygame.math.Vector2, attack_type: str, groups: Union[Sequence[pygame.sprite.Group], pygame.sprite.Group]) -> None:
        self.attack_type = attack_type
        super().__init__(groups, pos, 'moving')

        if self.attack_type == 'magic_wand':
            self.direction = direction
            self.lifetime = Timer(duration=5000, func=self.kill)
            self.lifetime.activate()
            self.movement_speed = 150
            self.damage = 500

    def import_frames(self) -> dict[str: list[pygame.Surface]]:
        return {'moving': import_images_from_folder(f'./assets/animation_frames/attacks/{self.attack_type}/moving/')}

    def update(self, dt):
        self.lifetime.update()
        self.animate(dt)
        self.move(dt)
