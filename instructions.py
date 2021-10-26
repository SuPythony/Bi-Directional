import os
import pygame
from button import Button


class Instructions:
    def __init__(self, surf, go_back):
        self.surf = surf
        self.go_back = go_back
        self.bg = pygame.transform.scale(pygame.image.load("assets/bg.png"), (900, 600))
        self.font = pygame.font.Font(os.path.join("assets", "fonts", "8BitOperatorPlus-Bold.ttf"), 30)
        self.heading_font = pygame.font.Font(os.path.join("assets", "fonts", "8BitOperatorPlus-Bold.ttf"), 50)
        self.instruct_font = pygame.font.Font(os.path.join("assets", "fonts", "8BitOperatorPlus-Bold.ttf"), 15)
        self.quit_button = Button(self.surf, os.path.join("assets", "buttons", "quit.png"),
                                  os.path.join("assets", "buttons", "quit_clicked.png"), (150, 50), "Close",
                                  self.go_back)
        self.quit_button.button_pos = (self.surf.get_rect().w - self.quit_button.normal.get_rect().w - 20, 20)
        page1 = [
            "Welcome to Bi-Directional, a multiview",
            "2d shooter game!",
            "",
            "You play as space explorer trapped in a",
            "spaceship filled with aliens who are",
            "eager to kill you.",
            "",
            "The aliens have a special ability...",
            "they are visible only from one side - ",
            "the side closest to them."
        ]
        page2 = [
            "Objective colorb",
            "",
            "You need to kill and overcome all",
            "the enemies to reach to the control room,",
            "but the enemies just keep coming,",
            "more and more.",
            "",
            "Try to kill as many enemies as you can and",
            "break your highscore!"
        ]
        page3 = [
            "Gameplay - 1 colorb",
            "",
            "You can see two views of the ship -",
            "One from the left side of the player and the",
            "other from the right. The screen is divided",
            "into two areas horizontally. The area above is",
            "your left side and the are below is the right",
            "side. The aliens, with their special power ",
            "are visible only on one side at a time."
        ]
        page4 = [
            "Gameplay - 2 colorb",
            "",
            "You need to choose the correct side and",
            "kill the enemies. The selected side is",
            "highlighted with green.",
            "",
            "After scoring 30 points you get the",
            "ability to shoot diagonally, on the",
            "side not selected."
        ]
        page5 = [
            "Gameplay - 3 colorb",
            "",
            "On every direct shot you lose 1 ammo.",
            "On a diagonal shot, you lose 2 ammo.",
            "To restore your ammo - Kill enemies",
            "and score points. Yes! Killing",
            "enemies gives you some ammo",
            "and for every 10 points scored, you",
            "receive some extra ammo."
        ]
        page6 = [
            "Controls colorb",
            "",
            "Move - Left and Right Arrow keys",
            "or A and D",
            "Change Side - Up Arrow Key or W",
            "Shoot - Space Bar",
            "Shoot Diagonally - X",
            "Exit game to home screen - Escape"
        ]
        page7 = [
            "Now you are ready to go! colorb",
            "",
            "Kill the aliens, don't die and",
            "try to break your high score!",
            "",
            "Remember - the game becomes",
            "progressively difficult as",
            "you score."
        ]
        self.pages = [page1, page2, page3, page4, page5, page6, page7]
        self.y = 80
        self.page = 1
        self.key_used = False

    def draw(self):
        self.surf.blit(self.bg, (0, 0))
        self.quit_button.draw()
        if not self.key_used:
            self.surf.blit(self.instruct_font.render("Use arrow keys to change the page", True, "white"), (20, 30))
        text = self.font.render(f"{self.page} of {len(self.pages)}", True, "white")
        self.surf.blit(text, ((self.surf.get_rect().w - text.get_rect().w) // 2, 20))
        for t in self.pages[self.page - 1]:
            if t.endswith("colorb"):
                text = self.heading_font.render(" ".join(t.split(" ")[:-1]), True, "#9e21de")
            else:
                text = self.font.render(t, True,
                                        "white")
            self.surf.blit(text, ((self.surf.get_rect().w - text.get_rect().w) // 2, self.y))
            self.y += text.get_rect().h + 10
        self.y = 80

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.go_back()
            elif event.key == pygame.K_RIGHT:
                self.key_used = True
                self.page += 1
                if self.page > len(self.pages):
                    self.page = len(self.pages)
            elif event.key == pygame.K_LEFT:
                self.key_used = True
                self.page -= 1
                if self.page < 1:
                    self.page = 1
        elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEMOTION:
            self.quit_button.on_event(event)
