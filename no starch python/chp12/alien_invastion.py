import sys
import pygame
# importing the needed modules

def run_game():
    #initalise game and create a screen object
    pygame.init() #initalises background settings needed for game to run
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Alien invasion")

    # main loop for the game
    while True:

        # for kbm movements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.flip()

run_game()