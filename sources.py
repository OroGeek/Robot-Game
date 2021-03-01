from pygame import image
from random import randint
from threading import Lock


class Sources():
    def __init__(self, window, settings, grid, sources_list):
        self.window = window
        self.settings = settings
        self.grid = grid
        self.size = settings.size_source
        self.img = image.load('icons/source.png')
        self.positon = 0
        self.sources_list = sources_list
        self.show()

    def get_position(self, x, y):
        return x*self.settings.cell_width + self.settings.margin, y*self.settings.cell_width + self.settings.margin

    def show(self):
        lock = Lock()
        size = len(self.grid) - 1
        index = randint(int(size / 2), size)

        lock.acquire()
        while self.grid[index].occuped:
            index = randint(int(size / 2), size)

        cell = self.grid[index]
        cell.occuped = True
        cell.type = "Source"
        self.positon = index
        self.window.blit(self.img, self.get_position(cell.i, cell.j))

        self.sources_list[self.get_position(cell.i, cell.j)] = self

        lock.release()

    def decrease(self):
        self.size -= 1
        cell = self.grid[self.positon]
        if self.size == 0:
            cell.show(self.window)
            cell.occuped = False
            cell.type = "Cell"
            self.sources_list.pop(self.get_position(cell.i, cell.j))
        return self.size
