import pygame as pg
import random

grid_size = 50
grid = [[0 for x in range(grid_size)] for x in range(grid_size)] 

pg.init()
win = pg.display.set_mode((500,500))
win.fill((255,255,255))

class node:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.visited = False
        self.top = True
        self.right = True
        self.bottom = True
        self.left = True
        self.neighbours = []

    def addNeighbours(self):
        if self.i > 0:
            self.neighbours.append(grid[self.i-1][self.j])
        if self.j > 0:
            self.neighbours.append(grid[self.i][self.j-1])
        if self.i < grid_size-1:
            self.neighbours.append(grid[self.i+1][self.j])
        if self.j < grid_size-1:
            self.neighbours.append(grid[self.i][self.j+1])

    def get_unvisited(self):
        temp = []
        for i in self.neighbours:
            if not i.visited:
                temp.append(i)
        return temp

    def show(self, color):
        w = 500//grid_size
        x = self.i * w
        y = self.j * w

        if self.top:
            pg.draw.line(win, color, (x, y), (x+w, y), 1)
        if self.right:
            pg.draw.line(win, color, (x+w, y), (x+w, y+w), 1)
        if self.bottom:
            pg.draw.line(win, color, (x+w, y+w), (x, y+w), 1)
        if self.left:
            pg.draw.line(win, color, (x, y+w), (x, y), 1)

for i in range(grid_size):
    for j in range(grid_size):
        grid[i][j] = node(i, j)

for i in range(grid_size):
    for j in range(grid_size):
        grid[i][j].addNeighbours()
        grid[i][j].show((0, 0, 0))
pg.display.update()

crashed = False
clock = pg.time.Clock()
start = grid[0][0]
stack = [start]
start.visited = True

while not crashed:
    win.fill((255,255,255))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            crashed = True
    for i in range(grid_size):
        for j in range(grid_size):
            grid[i][j].show((0, 0, 0))
    if stack:
        current = stack.pop()
        avail_nodes = current.get_unvisited()
        w = 500//grid_size
        pg.draw.rect(win, (255,0,255), (current.i*(w),current.j*(w),w,w))
        if avail_nodes:
            stack.append(current)
            chosen = random.choice(avail_nodes)
            x_grad = current.i - chosen.i
            y_grad = current.j - chosen.j

            if x_grad < 0:
                current.right = False
                chosen.left = False
            if x_grad > 0:
                current.left = False
                chosen.right = False
            if y_grad < 0:
                current.bottom = False
                chosen.top = False
            if y_grad > 0:
                current.top = False
                chosen.bottom = False

            chosen.visited = True
            stack.append(chosen)
    pg.display.update()
    clock.tick(60)