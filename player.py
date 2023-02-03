import pygame
from utils import import_images_from_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], groups: list[pygame.sprite.Group]):
        super().__init__(groups)

        self.animation_frames = self.load_frames()
        self.animation_speed = 5
        self.frame_index = 0
        self.status = Status(direction='down', action='idle')
        self.image = self.get_animation_frame_by_index(self.frame_index)

        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(self.rect.center)

        self.movement_speed = 250
        self.direction = pygame.math.Vector2(0, 0)

    def load_frames(self) -> dict[str: list[pygame.Surface]]:
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

    def get_direction_normalized(self) -> pygame.math.Vector2:
        keys = pygame.key.get_pressed()

        direction = pygame.math.Vector2(0, 0)
        if keys[pygame.K_UP]:
            direction.y = -1
        elif keys[pygame.K_DOWN]:
            direction.y = 1
        else:
            direction.y = 0

        if keys[pygame.K_LEFT]:
            direction.x = -1
        elif keys[pygame.K_RIGHT]:
            direction.x = 1
        else:
            direction.x = 0

        if direction.magnitude() > 0:
            direction = direction.normalize()

        return direction

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(self.animation_frames[str(self.status)]):
            self.frame_index = 0
        self.image = self.get_animation_frame_by_index(int(self.frame_index))

    def set_status(self):
        if self.direction.magnitude() == 0:
            action = 'idle'
        else:
            action = 'walk'
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

    def get_animation_frame_by_index(self, index: int) -> pygame.Surface:
        try:
            return self.animation_frames[str(self.status)][index]
        except IndexError:
            print(self.animation_frames)
            print(self.status, index)

    def move(self, dt):
        self.pos += (self.direction * self.movement_speed * dt)
        self.rect.center = self.pos

    def update(self, dt):
        self.direction = self.get_direction_normalized()
        self.move(dt)
        self.set_status()
        self.animate(dt)


class Status:
    def __init__(self, direction: str, action: str) -> None:
        self.direction = direction
        self.action = action

    def __str__(self) -> str:
        return f'{self.direction}_{self.action}'

    def __repr__(self) -> str:
        return f'{self.direction}_{self.action}'
