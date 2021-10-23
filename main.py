import pygame
from game import Game
from game_over import GameOver
from home_screen import HomeScreen

pygame.init()

WIDTH = 900
HEIGHT = 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("BYOG 2021 Game")

game = None
game_over = None
home_screen = None

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
    pygame.display.flip()


def start_game():
    global game, home_screen, game_over

    home_screen = None
    game_over = None

    ADD_ENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADD_ENEMY, 1500, 1)
    game = Game(WIN, WIDTH, HEIGHT, ADD_ENEMY, show_game_over, set_score)


def show_game_over():
    global game, home_screen, game_over

    home_screen = None
    game = None

    game_over = GameOver(WIN, score, show_home_screen, start_game)


def show_home_screen():
    global game, home_screen, game_over

    game = None
    game_over = None

    home_screen = HomeScreen(WIN, start_game)


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
        redraw_screen()
        clock.tick(15)
    pygame.quit()


main()
