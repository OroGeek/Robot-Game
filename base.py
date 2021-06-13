from pygame import image
from queue import Queue
from threading import Thread
import socket


class Base:
    def __init__(self, window, settings, grid):
        self.window = window
        self.settings = settings
        self.grid = grid
        print("Init Base")
        self.img = image.load('icons/base.png')
        self.window.blit(self.img, self.get_position(0, 0))
        self.sendSignal()

    def get_position(self, x, y):
        return x*self.settings.cell_width + self.settings.margin, y*self.settings.cell_width + self.settings.margin

    def sendPosition(self, s, position):
        header = 64

        msg = str(position).encode('utf-8')
        send_length = str(len(msg)).encode('utf-8')
        send_length += b' ' * (header - len(send_length))

        s.send(send_length)
        s.send(msg)

    def receivePostion(self, s):
        header = 64
        msg_length = s.recv(header).decode('utf-8')
        if msg_length:
            msg_length = int(msg_length)
            position = s.recv(msg_length).decode('utf-8')
            position = int(position)
            return position

    def sendSignal(self):
        s = socket.socket()
        s.bind(('localhost', 9999))
        s.listen()
        while True:
            cli, _ = s.accept()
            thread = Thread(
                target=self.sendtoclient, args=(cli,), daemon=True)
            thread.start()

    def sendtoclient(self, s):
        position = self.receivePostion(s)
        while position == None:
            position = self.receivePostion(s)
        shortPath = self.shortPath(position)
        for i in range(1, len(shortPath)):
            dose = round((len(shortPath) - i) / len(shortPath), 2)
            self.sendPosition(s, dose)
            self.sendPosition(s, shortPath[i])
        s.close()

    def explore_neighbours(self, index):
        cell = self.grid[index]

        if not cell.walls[0]:
            if index - self.settings.num_cols >= 0:
                nindex = index - self.settings.num_cols
                self.check(nindex, index)

        if not cell.walls[1]:
            if index + 1 < len(self.grid):
                nindex = index + 1
                self.check(nindex, index)

        if not cell.walls[2]:
            if index + self.settings.num_cols < len(self.grid):
                nindex = index + self.settings.num_cols
                self.check(nindex, index)

        if not cell.walls[3]:
            if index - 1 >= 0:
                nindex = index - 1
                self.check(nindex, index)

    def check(self, nindex, index):
        if self.visited[nindex] or self.grid[nindex].type == 'Source':
            return

        self.start.put(nindex)
        self.visited[nindex] = True
        self.prev[nindex] = index
        self.nodes_in_next_layer += 1

    def reconsructPath(self):
        path = []
        at = 0
        while at != None:
            path.append(at)
            at = self.prev[at]
        path.reverse()
        return path

    def shortPath(self, index):

        self.start = Queue()

        move_count = 0
        nodes_left_in_layer = 1
        self.nodes_in_next_layer = 0

        reached_end = False
        self.visited = [False for _ in range(len(self.grid))]
        self.prev = [None for _ in range(len(self.grid))]

        self.start.put(index)
        self.visited[index] = True

        while not self.start.empty():
            nindex = self.start.get()
            if nindex == 0:
                reached_end = True
                break
            self.explore_neighbours(nindex)

            nodes_left_in_layer -= 1
            if nodes_left_in_layer == 0:
                nodes_left_in_layer = self.nodes_in_next_layer
                self.nodes_in_next_layer = 0
                move_count += 1
        if reached_end:
            return self.reconsructPath()
