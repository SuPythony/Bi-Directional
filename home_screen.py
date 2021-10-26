import pygame
import os
from button import Button


class HomeScreen:
    def __init__(self, surf, start_game, show_instructions, show_credits):
        self.surf = surf
        self.start_game = start_game
        self.show_instructions = show_instructions
        self.show_credits = show_credits
        self.bg = pygame.image.load(os.path.join("assets", "menu_bg.png"))
        self.font = pygame.font.Font(os.path.join("assets", "fonts", "8BitOperatorPlus-Bold.ttf"), 15)
        self.play_button = Button(self.surf, os.path.join("assets", "buttons", "play.png"),
                                  os.path.join("assets", "buttons", "play_clicked.png"), (240, 80), "Play",
                                  self.start_game, height_offset=-30)
        self.instructions_button = Button(self.surf, os.path.join("assets", "buttons", "instructions.png"),
                                          os.path.join("assets", "buttons", "instructions_clicked.png"), (240, 80),
                                          "Instructions", self.show_instructions, height_offset=80)

    def draw(self):
        self.surf.blit(self.bg, (0, 0))
        self.play_button.draw()
        self.instructions_button.draw()
        text = self.font.render("Press c for credits", True, "white")
        self.surf.blit(text, (
            (self.surf.get_rect().w - text.get_rect().w) // 2, self.surf.get_rect().h - text.get_rect().h - 20))

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                self.show_credits()
        elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEMOTION:
            self.play_button.on_event(event)
            self.instructions_button.on_event(event)
