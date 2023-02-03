import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], groups: list[pygame.sprite.Group]):
        super().__init__(groups)
        self.image = pygame.Surface((32, 32))
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(self.rect.center)

        self.movement_speed = 250
        self.direction = pygame.math.Vector2(0, 0)

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

    def move(self, dt):
        self.pos += (self.direction * self.movement_speed * dt)
        self.rect.center = self.pos

    def update(self, dt):
        self.direction = self.get_direction_normalized()
        self.move(dt)
