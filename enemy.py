import pygame
import os
import random


class Enemy:
    def __init__(self, surf, remove_enemy):
        self.surf = surf
        self.running_images = []
        self.standing_images = []
        self.dying_images = []
        self.biting_images = []
        self.moving = True
        self.standing = False
        self.dying = False
        self.biting = False
        for i in range(1, 6):
            self.running_images.append(
                pygame.transform.scale(pygame.image.load(
                    os.path.join("assets", "enemy", "running", f"scifi_alien_run_{i}.png")), (200, 100)))
            self.running_images.append(
                pygame.transform.scale(pygame.image.load(
                    os.path.join("assets", "enemy", "running", f"scifi_alien_run_{i}.png")), (200, 100)))
        for i in range(1, 3):
            self.standing_images.append(
                pygame.transform.scale(pygame.image.load(
                    os.path.join("assets", "enemy", "standing", f"scifi_alien_idle_{i}.png")), (200, 100)))
        for i in range(1, 6):
            self.dying_images.append(
                pygame.transform.scale(pygame.image.load(
                    os.path.join("assets", "enemy", "dying", f"scifi_alien_die_{i}.png")), (200, 100)))
        for i in range(1, 6):
            self.biting_images.append(
                pygame.transform.scale(pygame.image.load(
                    os.path.join("assets", "enemy", "biting", f"scifi_alien_bite_{i}.png")), (200, 100)))
        self.lane = random.choice(["left", "right"])
        self.running_image_index = 0
        self.standing_image_index = 0
        self.dying_image_index = 0
        self.biting_image_index = 0
        self.image = self.standing_images[self.standing_image_index]
        self.mask = pygame.mask.from_surface(self.image)
        self.x = self.surf.get_rect().w
        self.y = 130 if self.lane == "left" else 430
        self.remove_enemy = remove_enemy

    def draw(self):
        if self.biting:
            self.biting_image_index += 1
            if self.biting_image_index > len(self.biting_images) - 1:
                self.biting = False
                self.standing = True
            else:
                self.image = self.biting_images[self.biting_image_index]
        elif self.standing:
            self.standing_image_index = (self.standing_image_index + 1) % len(self.standing_images)
            self.image = self.standing_images[self.standing_image_index]
        elif self.moving:
            self.running_image_index = (self.running_image_index + 1) % len(self.running_images)
            self.image = self.running_images[self.running_image_index]
        elif self.dying:
            self.dying_image_index += 1
            if self.dying_image_index > len(self.dying_images) - 1:
                self.remove_enemy(self)
                return
            self.image = self.dying_images[self.dying_image_index]
        self.mask = pygame.mask.from_surface(self.image)
        self.surf.blit(self.image, (self.x, self.y))
