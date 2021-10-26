import pygame
import os
import random
from utils import check_collision
from player import Player
from enemy import Enemy
from platform import Platform
from ammo_indicator import AmmoIndicator


class Game:
    def __init__(self, surf, win_width, win_height, add_enemy_event, show_game_over, set_score, goto_home_screen):
        self.surf = surf
        self.bg_img = pygame.transform.scale(pygame.image.load("assets/bg.png"), (win_width, win_height))
        self.win_width = win_width
        self.win_height = win_height
        self.set_score = set_score
        self.show_game_over = show_game_over
        self.goto_home_screen = goto_home_screen
        self.player_x = 20
        self.left_player = Player(self.surf, "left", self.game_over)
        self.right_player = Player(self.surf, "right", self.game_over)
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
        self.ammo = 10
        self.ammo_indicator = AmmoIndicator(self.surf)
        self.increase_difficulty = pygame.USEREVENT + 2
        pygame.time.set_timer(self.increase_difficulty, 7500)

    def game_over(self):
        self.set_score(self.score)
        self.show_game_over()

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
        self.surf.blit(self.bg_img, (0, self.surf.get_rect().h // 2))
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
                        if self.score % 10 == 0:
                            self.ammo += random.randint(3, 5)
                        if self.ammo <= 5:
                            self.ammo += random.randint(1, 2)
                        if self.ammo > 20:
                            self.ammo = 20
        for bullet in self.right_player.bullets:
            for enemy in self.enemies:
                if not enemy.dying:
                    if check_collision(enemy, bullet):
                        bullet.hit = True
                        enemy.dying = True
                        enemy.standing = False
                        enemy.moving = False
                        self.score += 1
                        if self.score % 10 == 0:
                            self.ammo += random.randint(3, 5)
                        if self.ammo <= 5:
                            self.ammo += random.randint(1, 2)
                        if self.ammo > 20:
                            self.ammo = 20
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
        self.ammo_indicator.draw(self.ammo)

        pygame.draw.rect(self.surf, "white", (0, self.surf.get_rect().h // 2, self.surf.get_rect().w, 3))
        if self.lane == "right":
            pygame.draw.rect(self.surf, "green",
                             (0, self.surf.get_rect().h // 2, self.surf.get_rect().w, self.surf.get_rect().h // 2), 3)
        elif self.lane == "left":
            pygame.draw.rect(self.surf, "green", (0, 0, self.surf.get_rect().w, self.surf.get_rect().h // 2), 3)

    def on_event(self, event):
        if not self.left_player.dying:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.goto_home_screen()
                elif event.key == pygame.K_x:
                    if self.score >= 30:
                        if self.ammo > 0:
                            if self.lane == "left":
                                self.right_player.shoot(True)
                                self.left_player.shoot(False)
                                self.ammo -= 2
                            else:
                                self.left_player.shoot(True)
                                self.right_player.shoot(False)
                                self.ammo -= 2
                elif event.key == pygame.K_SPACE:
                    if self.ammo > 0:
                        if self.lane == "left":
                            self.left_player.shoot(True)
                            self.right_player.shoot(False)
                            self.ammo -= 1
                        else:
                            self.right_player.shoot(True)
                            self.left_player.shoot(False)
                            self.ammo -= 1
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.lane = "left" if self.lane == "right" else "right"
                    self.left_player.lane_changed(self.lane)
                    self.right_player.lane_changed(self.lane)
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
