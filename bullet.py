import pygame
import os


class Bullet:
    def __init__(self, surf, remove_bullet):
        self.surf = surf
        self.images = []
        self.hit_images = []
        for i in range(1, 3):
            self.images.append(
                pygame.transform.scale(pygame.image.load(
                    os.path.join("assets", "bullet", f"scifi_blasterfire_{i}.png")), (28, 5)))
        for i in range(1, 5):
            self.hit_images.append(
                pygame.transform.scale(pygame.image.load(
                    os.path.join("assets", "bullet", "hit", f"scifi_blasterimpact_{i}.png")), (38, 56)))
        self.image_index = 0
        self.hit_image_index = 0
        self.image = self.images[self.image_index]
        self.hit = False
        self.x = 0
        self.drawn_once = False
        self.mask = pygame.mask.from_surface(self.image)
        self.y = 0
        self.remove_bullet = remove_bullet

    def draw(self, x, y):
        if self.hit:
            self.hit_image_index += 1
            if self.hit_image_index > len(self.hit_images) - 1:
                self.remove_bullet(self)
                self.hit = False
            else:
                self.image = self.hit_images[self.hit_image_index]
        else:
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]
        self.mask = pygame.mask.from_surface(self.image)
        self.x = x
        self.y = y
        self.surf.blit(self.image, (x, y))
