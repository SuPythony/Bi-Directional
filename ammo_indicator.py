import pygame
import os


class AmmoIndicator:
    def __init__(self, surf):
        self.surf = surf
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "ammo", "indicator.png")),
                                            (10, 28))

    def draw(self, ammo):
        x = 20
        for i in range(ammo):
            self.surf.blit(self.image, (x, 20))
            if ammo <= 3:
                red = pygame.Surface(self.image.get_rect().size).convert_alpha()
                red.fill((255, 0, 0, 50))
                self.surf.blit(red, (x, 20))
            x += self.image.get_rect().w + 10
