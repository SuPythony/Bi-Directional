import pygame
import os


class Platform:
    def __init__(self, surf):
        self.surf = surf
        self.images = []
        self.images.append(
            pygame.transform.scale(pygame.image.load(os.path.join("assets", "platforms", "PlatformBolts.png")),
                                   (70, 70)))
        self.images.append(
            pygame.transform.scale(pygame.image.load(os.path.join("assets", "platforms", "PlatformBlank.png")),
                                   (70, 70)))

    def draw(self):
        x = 0
        img_index = 0
        while x < self.surf.get_rect().w:
            self.surf.blit(self.images[img_index],
                           (x, self.surf.get_rect().h // 2 - self.images[img_index].get_rect().h))
            x += self.images[img_index].get_rect().w
            img_index += 1
            if img_index > 1:
                img_index = 0
        x = 0
        img_index = 0
        while x < self.surf.get_rect().w:
            self.surf.blit(self.images[img_index], (x, self.surf.get_rect().h - self.images[img_index].get_rect().h))
            x += self.images[img_index].get_rect().w
            img_index += 1
            if img_index > 1:
                img_index = 0
