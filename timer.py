from typing import Callable

import pygame


class Timer:
    def __init__(self, duration: int, func: Callable = None):
        self.duration = duration
        self.func = func
        self.start_time = 0
        self.active = False

    def activate(self) -> None:
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self) -> None:
        self.active = False
        self.start_time = 0

    def update(self) -> None:
        if self.active:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.duration:
                if self.func and self.start_time != 0:
                    self.func()
                self.deactivate()
