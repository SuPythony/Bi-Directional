import pygame
from game import Game
from game_over import GameOver

pygame.init()

WIDTH = 900
HEIGHT = 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("BYOG 2021 Game")

game = None
game_over = None


def redraw_screen():
    WIN.fill("white")
    if game:
        game.draw()
    if game_over:
        game_over.draw()
    pygame.display.flip()


def start_game():
    global game

    ADD_ENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADD_ENEMY, 1500, 1)
    game = Game(WIN, WIDTH, HEIGHT, ADD_ENEMY, show_game_over)


def show_game_over():
    global game_over

    game_over = GameOver(WIN, 0)


def main():
    running = True
    clock = pygame.time.Clock()
    start_game()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game:
                game.on_event(event)
        redraw_screen()
        clock.tick(15)
    pygame.quit()


main()
