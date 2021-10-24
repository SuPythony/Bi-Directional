import pygame
import os


class Credits:
    def __init__(self, surf, go_back):
        self.surf = surf
        self.go_back = go_back
        self.bg = pygame.transform.scale(pygame.image.load("assets/bg.png"), (900, 600))
        self.font = pygame.font.Font(os.path.join("assets", "fonts", "8BitOperatorPlus-Bold.ttf"), 30)
        self.y = surf.get_rect().h
        self.credits = [
            "Bi-Directional",
            "",
            "Made for BYOG 2021 Game Jam",
            "",
            "Programmed by Sumanyu Aggarwal",
            "Art created and edited by ",
            "Music given by Tejas Chichkar",
            "",
            "Additional credits in credits.txt",
            "",
            "Thanks for playing!"
        ]

    def draw(self):
        self.surf.blit(self.bg, (0, 0))
        y = self.y
        for t in self.credits:
            text = self.font.render(t, True, "white")
            self.surf.blit(text, ((self.surf.get_rect().w - text.get_rect().w) // 2, y))
            y += text.get_rect().h + 5
        self.y -= 5
        if self.y < -530:
            self.go_back()

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.go_back()
