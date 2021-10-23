import pygame
import os


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

        self.home = pygame.transform.scale(pygame.image.load(os.path.join("assets", "buttons", "home.png")), (168, 120))
        self.home_clicked = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "buttons", "home_clicked.png")), (168, 120))
        self.home_is_clicked = False
        self.restart = pygame.transform.scale(pygame.image.load(os.path.join("assets", "buttons", "restart.png")),
                                              (168, 120))
        self.restart_clicked = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "buttons", "restart_clicked.png")), (168, 120))
        self.restart_is_clicked = False
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
        self.surf.blit(self.home if not self.home_is_clicked else self.home_clicked,
                       ((self.surf.get_rect().w // 2 - self.home.get_rect().w) // 2, 460))
        self.surf.blit(self.restart if not self.restart_is_clicked else self.restart_clicked, (
            self.surf.get_rect().w // 2 + (self.surf.get_rect().w // 2 - self.home.get_rect().w) // 2, 460))

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if pygame.Rect(((self.surf.get_rect().w // 2 - self.home.get_rect().w) // 2, 460,
                            self.home.get_rect().w, self.home.get_rect().h)).collidepoint(x, y):
                self.home_is_clicked = True
            elif pygame.Rect((
                    self.surf.get_rect().w // 2 + (self.surf.get_rect().w // 2 - self.home.get_rect().w) // 2, 460,
                    self.restart.get_rect().w, self.restart.get_rect().h)).collidepoint(x, y):
                self.restart_is_clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            if pygame.Rect(((self.surf.get_rect().w // 2 - self.home.get_rect().w) // 2, 460,
                            self.home.get_rect().w, self.home.get_rect().h)).collidepoint(x, y):
                if self.home_is_clicked:
                    self.home_is_clicked = False
                    self.goto_home()
            elif pygame.Rect((
                    self.surf.get_rect().w // 2 + (self.surf.get_rect().w // 2 - self.home.get_rect().w) // 2, 460,
                    self.restart.get_rect().w, self.restart.get_rect().h)).collidepoint(x, y):
                if self.restart_is_clicked:
                    self.restart_is_clicked = False
                    self.restart_game()
