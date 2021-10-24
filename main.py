import os
import sys

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

import pygame
from game import Game
from game_over import GameOver
from home_screen import HomeScreen
from instructions import Instructions
from credits import Credits

pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH = 900
HEIGHT = 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("BYOG 2021 Game")
pygame.display.set_icon(pygame.image.load(os.path.join("assets", "icon.ico")))

game = None
game_over = None
home_screen = None
instructions = None
game_credits = None

score = 0


def set_score(new_score):
    global score

    score = new_score


def redraw_screen():
    WIN.fill("white")
    if game:
        game.draw()
    if game_over:
        game_over.draw()
    if home_screen:
        home_screen.draw()
    if instructions:
        instructions.draw()
    if game_credits:
        game_credits.draw()
    pygame.display.flip()


def start_game():
    global game, home_screen, game_over, instructions, game_credits

    home_screen = None
    game_over = None
    instructions = None
    game_credits = None

    ADD_ENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADD_ENEMY, 1500, 1)
    game = Game(WIN, WIDTH, HEIGHT, ADD_ENEMY, show_game_over, set_score, show_home_screen)
    pygame.mixer.music.load(os.path.join("assets", "sounds", "game_music.ogg"))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.3)


def show_game_over():
    global game, home_screen, game_over, instructions, game_credits

    home_screen = None
    game = None
    instructions = None
    game_credits = None

    game_over = GameOver(WIN, score, show_home_screen, start_game)


def show_home_screen():
    global game, home_screen, game_over, instructions, game_credits

    game = None
    game_over = None
    if instructions is None and game_credits is None:
        play = True
    else:
        play = False
    instructions = None
    game_credits = None

    home_screen = HomeScreen(WIN, start_game, show_instructions, show_credits)
    if play:
        pygame.mixer.music.load(os.path.join("assets", "sounds", "background_music.mp3"))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(1)


def show_instructions():
    global game, home_screen, game_over, instructions, game_credits

    game = None
    game_over = None
    home_screen = None
    game_credits = None

    instructions = Instructions(WIN, show_home_screen)


def show_credits():
    global game, home_screen, game_over, instructions, game_credits

    game = None
    game_over = None
    home_screen = None
    instructions = None

    game_credits = Credits(WIN, show_home_screen)


def main():
    running = True
    clock = pygame.time.Clock()
    show_home_screen()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game:
                game.on_event(event)
            if home_screen:
                home_screen.on_event(event)
            if game_over:
                game_over.on_event(event)
            if instructions:
                instructions.on_event(event)
            if game_credits:
                game_credits.on_event(event)
        redraw_screen()
        clock.tick(15)
    pygame.quit()


main()
