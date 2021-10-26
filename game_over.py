import pygame
import os
from button import Button


class GameOver:
    def __init__(self, surf, score, goto_home, restart_game):
        self.surf = surf
        self.score = score
        self.goto_home = goto_home
        self.restart_game = restart_game
        self.bg_image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "bg.png")),
                                               self.surf.get_size())
        self.game_over_font = pygame.font.Font(os.path.join("assets", "fonts", "8BitOperatorPlus-Bold.ttf"), 100)
        self.score_font = pygame.font.Font(os.path.join("assets", "fonts", "8BitOperatorPlus-Bold.ttf"), 70)
        self.high_score_font = pygame.font.Font(os.path.join("assets", "fonts", "8BitOperatorPlus-Bold.ttf"), 60)
        self.new_high_score_font = pygame.font.Font(os.path.join("assets", "fonts", "8BitOperatorPlus-Bold.ttf"), 50)

        self.home_button = Button(self.surf, os.path.join("assets", "buttons", "home.png"),
                                  os.path.join("assets", "buttons", "home_clicked.png"), (168, 120), "Home",
                                  self.goto_home)
        self.home_button.button_pos = ((self.surf.get_rect().w // 2 - self.home_button.normal.get_rect().w) // 2, 460)
        self.restart_button = Button(self.surf, os.path.join("assets", "buttons", "restart.png"),
                                     os.path.join("assets", "buttons", "restart_clicked.png"), (168, 120), "Restart",
                                     self.restart_game)
        self.restart_button.button_pos = (
            self.surf.get_rect().w // 2 + (self.surf.get_rect().w // 2 - self.home_button.normal.get_rect().w) // 2,
            460)
        self.highscore = 0
        self.new_highscore = True
        with open(os.path.join("assets", "highscore.txt"), "r") as f:
            data = f.read()
            if data == "":
                self.highscore = self.score
                if self.score == 0:
                    self.new_highscore = False
            elif int(data) < self.score:
                self.highscore = self.score
            else:
                self.new_highscore = False
                self.highscore = int(data)

    def draw(self):
        self.surf.blit(self.bg_image, (0, 0))
        bg = pygame.Surface(self.surf.get_size()).convert_alpha()
        bg.fill((255, 255, 255, 50))
        self.surf.blit(bg, (0, 0))
        text = self.game_over_font.render("GAME OVER!", True, "#d1eedc")
        self.surf.blit(text, ((self.surf.get_rect().w - text.get_rect().w) // 2, 20))
        text = self.score_font.render(f"Score: {self.score}", True, "white")
        self.surf.blit(text, ((self.surf.get_rect().w - text.get_rect().w) // 2, 170))
        if self.new_highscore:
            with open(os.path.join("assets", "highscore.txt"), "w") as f:
                f.write(str(self.score))
        text = self.high_score_font.render(f"High Score: {self.highscore}", True, "white")
        self.surf.blit(text, ((self.surf.get_rect().w - text.get_rect().w) // 2, 270))
        if self.new_highscore:
            text = self.new_high_score_font.render("New High Score!", True, "white")
            self.surf.blit(text, ((self.surf.get_rect().w - text.get_rect().w) // 2, 350))
        self.home_button.draw()
        self.restart_button.draw()

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEMOTION:
            self.home_button.on_event(event)
            self.restart_button.on_event(event)
