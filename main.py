import pygame
import sys
from threading import Thread
from settings import Settings
from pygame.locals import *
from maze import *
from robot import *
from base import *
from sources import *

if __name__ == '__main__':
    pygame.init()
    settings = Settings()

    if settings.valid:

        window = pygame.display.set_mode(settings.size)
        pygame.display.set_caption('Robot Game')

        draw = True
        robots = []
        sources_list = {}

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            if draw:
                grid = drawMaze(window, settings)
                thread = Thread(target=Base, args=(
                    window, settings, grid), daemon=True)
                thread.start()

                # occuped by base
                grid[0].occuped = True
                grid[0].type = "Base"

                for _ in range(settings.sources):
                    thread = Thread(target=Sources, args=(
                        window, settings, grid, sources_list), daemon=True)
                    thread.start()

                for _ in range(settings.robots):
                    thread = Thread(target=Robot, args=(
                        window, settings, grid, sources_list), daemon=True)
                    robots.append(thread)
                    thread.start()
                draw = False

            end = True
            for thread in robots:
                if thread.is_alive():
                    end = False

            if end:
                print("END GAME")
                break
            pygame.display.update()
