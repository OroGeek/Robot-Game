from pygame import image
from random import choice
from time import sleep
from threading import Lock
import socket


class Robot:

    def __init__(self, window, settings, grid, sources_list):
        self.window = window
        self.settings = settings
        self.grid = grid
        self.position = 0
        self.img = image.load('icons/robot.png')
        self.grid[0].occuped = True
        self.visited = [True if i ==
                        0 else False for i in range(len(self.grid))]
        self.sources_list = sources_list
        self.Move()

    def get_position(self, x, y):
        return x*self.settings.cell_width + self.settings.margin, y*self.settings.cell_width + self.settings.margin

    def send(self, s):
        header = 64

        msg = str(self.position).encode('utf-8')
        send_length = str(len(msg)).encode('utf-8')
        send_length += b' ' * (header - len(send_length))

        s.send(send_length)
        s.send(msg)

    def receive(self, s):
        header = 64
        msg_length = s.recv(header).decode('utf-8')
        if msg_length:
            msg_length = int(msg_length)
            position = s.recv(msg_length).decode('utf-8')
            position = float(position)
            return position

    def randomMove(self):
        cell = self.grid[self.position]
        position = choice([i for i in range(4) if not cell.walls[i]])

        if position == 0:
            position = self.position - self.settings.num_cols
        elif position == 1:
            position = self.position + 1
        elif position == 2:
            position = self.position + self.settings.num_cols
        elif position == 3:
            position = self.position - 1

        return position

    def returnBase(self, disposePheromone):
        while self.position != 0:
            dose = self.receive(self.server)
            while dose == None:
                dose = self.receive(self.server)
            position = int(self.receive(self.server))
            while position == None:
                position = int(self.receive(self.server))
            old_position = self.position
            if disposePheromone:
                self.grid[old_position].disposePheromone(dose)
            yield position

    def followPheromone(self):
        position = self.position
        init_dose = self.grid[position].dose
        dose = init_dose

        victor = [-self.settings.num_cols, 1, self.settings.num_cols, -1]
        sourceFound = True
        sourceIndex = 0

        for i in range(4):
            index = self.position + victor[i]
            if index < 1 or index >= len(self.grid):
                continue
            cell = self.grid[index]

            if cell.type == 'Source':
                sourceIndex = index

            if cell.pheromone and cell.dose > dose:
                sourceFound = False
                dose = cell.dose
                position = index

        if init_dose == dose and sourceIndex == 0:
            position = self.randomMove()
            return position
        if sourceFound:
            return sourceIndex
        else:
            return position

    position_sended = False
    isReturning = False
    disposePheromone = False
    sourceFound = False
    end = False

    def actionToDo(self):
        if self.position == 0:
            self.isReturning = False
            self.disposePheromone = False
            self.sourceFound = False
            self.visited = [True if i ==
                            0 else False for i in range(len(self.grid))]
            self.position_sended = False
            position = self.randomMove()

            self.server = socket.socket()
            self.server.connect(('localhost', 9999))
        elif sum(self.visited) == len(self.grid) or self.sourceFound:
            # return Base
            if sum(self.visited) == len(self.grid):
                self.end = True
            self.isReturning = True
            if not self.position_sended:
                self.send(self.server)
                self.position_sended = True
            position = next(self.returnBase(self.disposePheromone))
        elif not self.isReturning and self.grid[self.position].pheromone:
            position = self.followPheromone()
        else:
            position = self.randomMove()

        return position

    def Move(self):
        while True:
            sleep(0.1)
            # Action to do
            position = self.actionToDo()
            if position == 0 and self.end:
                self.grid[self.position].show(self.window)
                break

            lock = Lock()
            cell = self.grid[position]
            lock.acquire()
            if not cell.occuped:
                cell.occuped = True
                cell.type = "Robot"
                if self.position != 0:
                    self.grid[self.position].occuped = False
                    if not self.disposePheromone:
                        self.grid[self.position].show(self.window)
                self.position = position
                self.visited[position] = True
                self.window.blit(self.img, self.get_position(cell.i, cell.j))
            else:
                if cell.type == "Source":
                    self.sources_list[self.get_position(
                        cell.i, cell.j)].decrease()
                    self.sourceFound = True
                    self.disposePheromone = True
                elif cell.type == "Base" and self.isReturning:
                    cell = self.grid[self.position]
                    cell.occuped = False
                    cell.show(self.window)
                    self.position = position
                    self.window.blit(
                        self.img, self.get_position(cell.i, cell.j))
            lock.release()
        self.server.close()
