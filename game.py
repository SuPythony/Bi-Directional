import pygame
import os
import random


def check_collision(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (int(offset_x), int(offset_y))) is not None


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


class Player:
    def __init__(self, surf, direction):
        self.surf = surf
        self.direction = direction
        self.running_images = []
        self.standing_images = []
        self.shooting_images = []
        self.dying_images = []
        for i in range(1, 7):
            self.running_images.append(
                pygame.transform.scale(pygame.image.load(
                    os.path.join("assets", "player", "running", direction, f"scifi_marine_run_{i}.png")), (150, 150)))
        for i in range(1, 3):
            self.standing_images.append(
                pygame.transform.scale(pygame.image.load(
                    os.path.join("assets", "player", "standing", direction, f"scifi_marine_stand_{i}.png")),
                    (150, 150)))
            self.standing_images.append(
                pygame.transform.scale(pygame.image.load(
                    os.path.join("assets", "player", "standing", direction, f"scifi_marine_stand_{i}.png")),
                    (150, 150)))
        for i in range(1, 3):
            self.shooting_images.append(
                pygame.transform.scale(pygame.image.load(
                    os.path.join("assets", "player", "shooting", direction, f"scifi_marine_shoot_{i}.png")),
                    (150, 150)))
        for i in range(1, 6):
            self.dying_images.append(
                pygame.transform.scale(pygame.image.load(
                    os.path.join("assets", "player", "dying", direction, f"scifi_marine_die_{i}.png")),
                    (150, 150)))
        self.running_image_index = 0
        self.standing_image_index = 0
        self.shooting_image_index = -1
        self.dying_image_index = -1
        self.image = self.standing_images[self.standing_image_index]
        self.mask = pygame.mask.from_surface(self.image)
        self.moving = False
        self.standing = True
        self.shooting = False
        self.dying = False
        self.bullets = []
        self.y = 80 if self.direction == "left" else 380
        self.x = 0

    def draw(self, x):
        self.x = x
        if self.dying:
            self.dying_image_index += 1
            if self.dying_image_index > len(self.dying_images) - 1:
                # player died game over
                pass
            else:
                self.image = self.dying_images[self.dying_image_index]
        elif self.shooting:
            self.shooting_image_index += 1
            if self.shooting_image_index > len(self.shooting_images) - 1:
                self.shooting_image_index = -1
                self.shooting = False
            else:
                self.image = self.shooting_images[self.shooting_image_index]
        elif self.standing:
            self.standing_image_index = (self.standing_image_index + 1) % len(self.standing_images)
            self.image = self.standing_images[self.standing_image_index]
        elif self.moving:
            self.running_image_index = (self.running_image_index + 1) % len(self.running_images)
            self.image = self.running_images[self.running_image_index]
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

    def shoot(self):
        bullet = Bullet(self.surf, self.remove_bullet)
        self.bullets.append(bullet)
        self.shooting = True


class Game:
    def __init__(self, surf, win_width, win_height, add_enemy_event):
        self.surf = surf
        self.bg_img = pygame.transform.scale(pygame.image.load("assets/bg.png"), (win_width, win_height))
        self.win_width = win_width
        self.win_height = win_height
        self.player_x = 20
        self.left_player = Player(self.surf, "left")
        self.right_player = Player(self.surf, "right")
        self.player_width = self.left_player.image.get_rect().w
        self.player_height = self.left_player.image.get_rect().h
        self.player_speed = 10
        self.pressed_left = False
        self.pressed_right = False
        self.lane = "right"
        self.enemies = []
        self.add_enemy_event = add_enemy_event
        self.added_first_enemy = False
        self.enemy_spawn_time = 3500
        self.enemy_speed = 5
        self.score_font = pygame.font.Font(os.path.join("assets", "fonts", "ka1.ttf"), 35)
        self.score = 0
        self.platform = Platform(self.surf)
        self.increase_difficulty = pygame.USEREVENT + 2
        pygame.time.set_timer(self.increase_difficulty, 7500)

    def remove_enemy(self, enemy):
        temp_enemies = self.enemies
        temp_enemies.remove(enemy)
        self.enemies = temp_enemies

    def draw(self):
        if self.pressed_left:
            if not self.left_player.dying:
                self.player_x -= self.player_speed
        elif self.pressed_right:
            if not self.left_player.dying:
                self.player_x += self.player_speed
        if self.player_x < 0:
            self.player_x = 0
            if self.left_player.moving:
                self.left_player.moving = False
                self.left_player.standing = True
                self.right_player.moving = False
                self.right_player.standing = True
        if self.player_x > self.win_width - self.player_width:
            self.player_x = self.win_width - self.player_width
            if self.left_player.moving:
                self.left_player.moving = False
                self.left_player.standing = True
                self.right_player.moving = False
                self.right_player.standing = True
        self.surf.blit(self.bg_img, (0, 0))
        for enemy in self.enemies:
            if check_collision(enemy, self.left_player) or check_collision(enemy, self.right_player):
                self.left_player.dying = True
                self.right_player.dying = True
                enemy.biting = True
        for bullet in self.left_player.bullets:
            for enemy in self.enemies:
                if not enemy.dying:
                    if check_collision(enemy, bullet):
                        bullet.hit = True
                        enemy.dying = True
                        enemy.standing = False
                        enemy.moving = False
                        self.score += 1
        for bullet in self.right_player.bullets:
            for enemy in self.enemies:
                if not enemy.dying:
                    if check_collision(enemy, bullet):
                        bullet.hit = True
                        enemy.dying = True
                        enemy.standing = False
                        enemy.moving = False
                        self.score += 1
        score_text = self.score_font.render(f"Score: {self.score}", True, "white")
        self.surf.blit(score_text, (self.surf.get_rect().w - 20 - score_text.get_rect().w, 20))
        self.left_player.draw(self.player_x)
        self.right_player.draw(self.player_x)
        for enemy in self.enemies:
            if not enemy.dying and not enemy.biting and not self.left_player.dying:
                enemy.x -= self.enemy_speed
            elif not enemy.biting and self.left_player.dying:
                enemy.standing = True
            enemy.draw()
        self.platform.draw()

        pygame.draw.rect(self.surf, "white", (0, self.surf.get_rect().h // 2, self.surf.get_rect().w, 3))
        if self.lane == "right":
            pygame.draw.rect(self.surf, "green",
                             (0, self.surf.get_rect().h // 2, self.surf.get_rect().w, self.surf.get_rect().h // 2), 3)
        elif self.lane == "left":
            pygame.draw.rect(self.surf, "green", (0, 0, self.surf.get_rect().w, self.surf.get_rect().h // 2), 3)

    def on_event(self, event):
        if not self.left_player.dying:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.lane == "left":
                        self.left_player.shoot()
                    else:
                        self.right_player.shoot()
                elif event.key == pygame.K_UP:
                    self.lane = "left" if self.lane == "right" else "right"
                elif event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d]:
                    self.left_player.moving = True
                    self.left_player.standing = False
                    self.left_player.shooting = False
                    self.right_player.moving = True
                    self.right_player.standing = False
                    self.right_player.shooting = False
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.pressed_left = True
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.pressed_right = True
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d]:
                    self.left_player.moving = False
                    self.left_player.standing = True
                    self.right_player.moving = False
                    self.right_player.standing = True
                    self.pressed_left = False
                    self.pressed_right = False
            elif event.type == self.add_enemy_event:
                if not self.added_first_enemy:
                    self.added_first_enemy = True
                pygame.time.set_timer(self.add_enemy_event, self.enemy_spawn_time)
                self.enemies.append(Enemy(self.surf, self.remove_enemy))
            elif event.type == self.increase_difficulty:
                self.enemy_speed += 1.5
                self.enemy_spawn_time -= 250
