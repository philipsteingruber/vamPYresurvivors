import pygame


class ExperienceGem(pygame.sprite.Sprite):
    def __init__(self, groups: pygame.sprite.Group, value: int, pos: tuple[int, int]):
        super().__init__(groups)
        self.value = value
        self.image = pygame.transform.scale_by(pygame.image.load('./assets/collectibles/xp_gems/blue_gem.png').convert_alpha(), 2)
        self.rect = self.image.get_rect(center=pos)
