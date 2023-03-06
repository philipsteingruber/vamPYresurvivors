import pygame
from typing import Union, Sequence
from timer import Timer


class KingBibleGenerator(pygame.sprite.Group):
    def __init__(self, groups: Union[Sequence[pygame.sprite.Group], pygame.sprite.Group], proj_count: int):
        super().__init__()
        self.groups = groups
        self.proj_count = proj_count
        self.initial_angles = self.calc_inital_angles(proj_count=self.proj_count)
        self.rotation_speed = 10
        self.radius = 50
        self.lifetime = Timer(3000, self.kill_all_sprites)
        self.cooldown = Timer(3000)

    @staticmethod
    def calc_inital_angles(proj_count: int) -> list[int]:
        region_size = 360 // proj_count
        return [0 + region_size * i for i in range(proj_count)]

    def kill_all_sprites(self):
        for sprite in self.sprites():
            sprite.kill()
        self.cooldown.activate()

    def create_sprites(self, player_pos):
        pass

    def update_sprites(self):
        pass

    def update(self, dt, player_pos: tuple):
        if self.lifetime.active:
            self.lifetime.update()
        if len(self.sprites()) > 0:  # Update the angle of the existing sprites
            self.update_sprites()
        else:  # Create new sprites
            if not self.cooldown.active:
                self.create_sprites(player_pos)
            else:
                self.cooldown.update()
