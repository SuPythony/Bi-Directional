import pygame
import os
from bullet import Bullet


class Player:
    def __init__(self, surf, direction, game_over):
        self.surf = surf
        self.direction = direction
        self.game_over = game_over
        self.running_images = {"selected": [], "unselected": []}
        self.standing_images = {"selected": [], "unselected": []}
        self.shooting_images = {"selected": [], "unselected": []}
        self.dying_images = {"selected": [], "unselected": []}
        for i in range(1, 7):
            image = pygame.transform.scale(pygame.image.load(
                os.path.join("assets", "player", "running", direction, f"scifi_marine_run_{i}.png")), (150, 150))
            self.running_images["unselected"].append(image)
            image2 = image.copy()
            for point in pygame.mask.from_surface(image).outline():
                image2.set_at(point, "green")
            self.running_images["selected"].append(image2)
        for i in range(1, 3):
            image = pygame.transform.scale(pygame.image.load(
                os.path.join("assets", "player", "standing", direction, f"scifi_marine_stand_{i}.png")), (150, 150))
            self.standing_images["unselected"].append(image)
            self.standing_images["unselected"].append(image)
            image2 = image.copy()
            for point in pygame.mask.from_surface(image).outline():
                image2.set_at(point, "green")
            self.standing_images["selected"].append(image2)
            self.standing_images["selected"].append(image2)
        for i in range(1, 3):
            image = pygame.transform.scale(pygame.image.load(
                os.path.join("assets", "player", "shooting", direction, f"scifi_marine_shoot_{i}.png")), (150, 150))
            self.shooting_images["unselected"].append(image)
            image2 = image.copy()
            for point in pygame.mask.from_surface(image).outline():
                image2.set_at(point, "green")
            self.shooting_images["selected"].append(image2)
        for i in range(1, 6):
            image = pygame.transform.scale(pygame.image.load(
                os.path.join("assets", "player", "dying", direction, f"scifi_marine_die_{i}.png")), (150, 150))
            self.dying_images["unselected"].append(image)
            image2 = image.copy()
            for point in pygame.mask.from_surface(image).outline():
                image2.set_at(point, "green")
            self.dying_images["selected"].append(image2)
        self.running_image_index = 0
        self.standing_image_index = 0
        self.shooting_image_index = -1
        self.dying_image_index = -1
        self.moving = False
        self.standing = True
        self.shooting = False
        self.dying = False
        self.bullets = []
        self.y = 80 if self.direction == "left" else 380
        self.x = 0
        self.bullet_fire = pygame.mixer.Sound(os.path.join("assets", "sounds", "bullet_fire.mp3"))
        if self.direction == "right":
            self.selected = True
        else:
            self.selected = False
        if self.selected:
            self.image = self.standing_images["selected"][self.standing_image_index]
        else:
            self.image = self.standing_images["unselected"][self.standing_image_index]
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, x):
        self.x = x
        if self.dying:
            self.dying_image_index += 1
            if self.dying_image_index > len(self.dying_images["selected"]) - 1:
                pygame.mixer.music.stop()
                pygame.mixer.Sound(os.path.join("assets", "sounds", "game_over.mp3")).play(0)
                pygame.time.delay(500)
                self.game_over()
            else:
                if self.selected:
                    self.image = self.dying_images["selected"][self.dying_image_index]
                else:
                    self.image = self.dying_images["unselected"][self.dying_image_index]
        elif self.shooting:
            self.shooting_image_index += 1
            if self.shooting_image_index > len(self.shooting_images["selected"]) - 1:
                self.shooting_image_index = -1
                self.shooting = False
            else:
                if self.selected:
                    self.image = self.shooting_images["selected"][self.shooting_image_index]
                else:
                    self.image = self.shooting_images["unselected"][self.shooting_image_index]
        elif self.standing:
            self.standing_image_index = (self.standing_image_index + 1) % len(self.standing_images["selected"])
            if self.selected:
                self.image = self.standing_images["selected"][self.standing_image_index]
            else:
                self.image = self.standing_images["unselected"][self.standing_image_index]
        elif self.moving:
            self.running_image_index = (self.running_image_index + 1) % len(self.running_images["selected"])
            if self.selected:
                self.image = self.running_images["selected"][self.running_image_index]
            else:
                self.image = self.running_images["unselected"][self.running_image_index]
        self.mask = pygame.mask.from_surface(self.image)
        self.surf.blit(self.image, (x, self.y))
        bullet_copy = self.bullets
        for bullet in self.bullets:
            if bullet.x > self.surf.get_rect().w:
                bullet_copy.remove(bullet)
                continue
            if bullet.drawn_once:
                if not bullet.hit:
                    bullet.x += 20
                bullet.draw(bullet.x, self.y + 90)
            else:
                bullet.draw(x + 105, self.y + 90)
                bullet.drawn_once = True
        self.bullets = bullet_copy

    def remove_bullet(self, bullet):
        temp_bullets = self.bullets
        temp_bullets.remove(bullet)
        self.bullets = temp_bullets

    def shoot(self, shoot_bullet):
        bullet = Bullet(self.surf, self.remove_bullet)
        self.shooting = True
        if shoot_bullet:
            self.bullets.append(bullet)
            self.bullet_fire.play()

    def lane_changed(self, lane):
        if lane == self.direction:
            self.selected = True
        else:
            self.selected = False
