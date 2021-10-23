import pygame
import os


class HomeScreen:
    def __init__(self, surf, start_game):
        self.surf = surf
        self.start_game = start_game
        self.bg = pygame.image.load(os.path.join("assets", "menu_bg.png"))
        self.play = pygame.transform.scale(pygame.image.load(os.path.join("assets", "buttons", "play.png")), (240, 80))
        self.instructions = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "buttons", "instructions.png")), (240, 80))
        self.play_clicked = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "buttons", "play_clicked.png")), (240, 80))
        self.instructions_clicked = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "buttons", "instructions_clicked.png")), (240, 80))
        self.play_is_clicked = False
        self.instructions_is_clicked = False

    def draw(self):
        self.surf.blit(self.bg, (0, 0))
        self.surf.blit(self.play if not self.play_is_clicked else self.play_clicked,
                       ((self.surf.get_rect().w - self.play.get_rect().w) // 2, self.surf.get_rect().h // 2 - 30))
        self.surf.blit(self.instructions if not self.instructions_is_clicked else self.instructions_clicked,
                       ((self.surf.get_rect().w - self.play.get_rect().w) // 2, self.surf.get_rect().h // 2 + 80))

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if pygame.Rect(((self.surf.get_rect().w - self.play.get_rect().w) // 2, self.surf.get_rect().h // 2 - 30,
                            self.play.get_rect().w, self.play.get_rect().h)).collidepoint(x, y):
                self.play_is_clicked = True
            elif pygame.Rect(((self.surf.get_rect().w - self.play.get_rect().w) // 2, self.surf.get_rect().h // 2 + 80,
                              self.play.get_rect().w, self.play.get_rect().h)).collidepoint(x, y):
                self.instructions_is_clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            if pygame.Rect(((self.surf.get_rect().w - self.play.get_rect().w) // 2, self.surf.get_rect().h // 2 - 30,
                            self.play.get_rect().w, self.play.get_rect().h)).collidepoint(x, y):
                if self.play_is_clicked:
                    self.play_is_clicked = False
                    self.start_game()
            elif pygame.Rect(((self.surf.get_rect().w - self.play.get_rect().w) // 2, self.surf.get_rect().h // 2 + 80,
                              self.play.get_rect().w, self.play.get_rect().h)).collidepoint(x, y):
                if self.instructions_is_clicked:
                    self.instructions_is_clicked = False
