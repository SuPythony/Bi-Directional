import pygame
import os


class GameOver:
    def __init__(self, surf, score):
        self.surf = surf
        self.score = score
        self.bg_image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "bg.png")),
                                               self.surf.get_size())
        self.game_over_font = pygame.font.Font(os.path.join("assets", "fonts", "8BitOperatorPlus-Bold.ttf"), 100)
        self.score_font = pygame.font.Font(os.path.join("assets", "fonts", "8BitOperatorPlus-Bold.ttf"), 70)
        self.high_score_font = pygame.font.Font(os.path.join("assets", "fonts", "8BitOperatorPlus-Bold.ttf"), 60)
        self.new_high_score_font = pygame.font.Font(os.path.join("assets", "fonts", "8BitOperatorPlus-Bold.ttf"), 50)

    def draw(self):
        self.surf.blit(self.bg_image, (0, 0))
        bg = pygame.Surface(self.surf.get_size()).convert_alpha()
        bg.fill((255, 255, 255, 50))
        self.surf.blit(bg, (0, 0))
        text = self.game_over_font.render("GAME OVER!", True, "#d1eedc")
        self.surf.blit(text, ((self.surf.get_rect().w - text.get_rect().w) // 2, 20))
        text = self.score_font.render(f"Score: {self.score}", True, "white")
        self.surf.blit(text, ((self.surf.get_rect().w - text.get_rect().w) // 2, 170))
        highscore = 0
        new_highscore = True
        with open(os.path.join("assets", "highscore.txt")) as f:
            data = f.read()
            if data == "":
                highscore = self.score
                if self.score == 0:
                    new_highscore = False
            elif int(data) < self.score:
                highscore = self.score
            else:
                new_highscore = False
                highscore = int(data)
        text = self.high_score_font.render(f"High Score: {highscore}", True, "white")
        self.surf.blit(text, ((self.surf.get_rect().w - text.get_rect().w) // 2, 270))
        if new_highscore:
            text = self.new_high_score_font.render("New High Score!", True, "white")
            self.surf.blit(text, ((self.surf.get_rect().w - text.get_rect().w) // 2, 350))
