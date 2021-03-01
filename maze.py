from os import get_inheritable
from threading import Thread
import pygame
from time import sleep
from random import randint


class Cell:
    def __init__(self, i, j, window):
        self.i, self.j = i, j
        self.walls = [False, False, False, False]
        self.visited = True
        self.occuped = False
        self.pheromone = False
        self.dose = 0
        self.window = window
        self.type = "Cell"

    def evaporisation(self):
        while True:
            if self.pheromone:
                self.dose *= 0.98
                if self.dose <= 0.1:
                    self.pheromone = False
                    self.dose = 0
                    self.show(self.window)
                    break

                x = self.i * cell_width + margin + 20
                y = self.j * cell_width + margin + 20
                pygame.draw.rect(self.window, (255 - self.dose*255, 255-self.dose*255, 255),
                                 (x, y, 10, 10))
            sleep(1)

    def disposePheromone(self, dose):
        self.pheromone = True
        self.dose = dose

        x = self.i * cell_width + margin + 20
        y = self.j * cell_width + margin + 20

        self.show(self.window)
        pygame.draw.rect(self.window, (255 - self.dose*255, 255-self.dose*255, 255),
                         (x, y, 10, 10))
        Thread(target=self.evaporisation, daemon=True).start()

    def show(self, window):
        x = self.i * cell_width + margin
        y = self.j * cell_width + margin

        if self.visited:
            pygame.draw.rect(window, (117, 69, 20),
                             (x, y, cell_width, cell_width))
        if self.walls[0]:
            pygame.draw.line(window, (255, 255, 255),
                             (x, y), (x + cell_width, y))
        if self.walls[1]:
            pygame.draw.line(window, (255, 255, 255), (x + cell_width, y),
                             (x+cell_width, y+cell_width))
        if self.walls[2]:
            pygame.draw.line(window, (255, 255, 255), (x+cell_width,
                                                       y+cell_width), (x, y + cell_width))
        if self.walls[3]:
            pygame.draw.line(window, (255, 255, 255),
                             (x, y + cell_width), (x, y))


def decresePheromone(grid):
    for cell in grid:
        cell.evaporisation()


def drawMaze(window, settings):
    global cell_width, margin, num_cols, num_rows, grid

    margin = settings.margin
    num_cols = settings.num_cols
    num_rows = settings.num_rows
    cell_width = settings.cell_width

    grid = []

    for j in range(num_rows):
        for i in range(num_cols):
            cell = Cell(i, j, window)
            grid.append(cell)

    for cell in grid:
        if cell.i == 0:
            cell.walls[3] = True
        if cell.i == num_cols - 1:
            cell.walls[1] = True
        if cell.j == 0:
            cell.walls[0] = True
        if cell.j == num_rows - 1:
            cell.walls[2] = True
        cell.show(window)

    addObstacles(window)

    return grid


def addObstacles(window):

    step = 2

    grid[0].walls[1] = True
    grid[1].walls[3] = True

    for i in range(2, len(grid)):
        if i % num_cols < 2:
            continue

        index = randint(0, 3)
        cell = grid[i]
        if step == 0:
            if index == 0:
                index = i - num_cols
                if index > 0:
                    cell.walls[0] = True
                    grid[index].walls[2] = True
            elif index == 1:
                index = i + 1
                if index < num_cols:
                    cell.walls[1] = True
                    grid[index].walls[3] = True
            elif index == 2:
                index = i + num_cols
                if index < num_rows:
                    cell.walls[2] = True
                    grid[index].walls[0] = True
            elif index == 3:
                index = i - 1
                if index > 0:
                    cell.walls[3] = True
                    grid[index].walls[1] = True
            step = 2
        else:
            step -= 1

    for cell in grid:
        cell.show(window)
