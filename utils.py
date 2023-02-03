import pygame
import os

'''
class Spritesheet:
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert()

    def image_at(self, rectangle, colorkey=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey=None):
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey=None):
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)
'''


def import_images_from_folder(path: str, scale_factor: float = 1, flip: bool = False) -> list[pygame.Surface]:
    surface_list = []

    for _, __, image_files in os.walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image = pygame.image.load(full_path).convert_alpha()

            image = pygame.transform.scale_by(image, scale_factor)
            image = pygame.transform.flip(image, flip_x=flip, flip_y=False)

            surface_list.append(image)

    return surface_list
