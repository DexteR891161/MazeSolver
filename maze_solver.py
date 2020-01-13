import pygame as pg
import random
import math

grid_size = 50
grid = [[0 for x in range(grid_size)] for x in range(grid_size)] 

pg.init()
win = pg.display.set_mode((500,500))
win.fill((255,255,255))

def heuristic(current, end):
    a = current.i-end.i
    b = current.j-end.j
    return math.sqrt(a**2 + b**2)

def reconstruct_path(cameFrom, current):
    total_path = [current]
    while current in cameFrom.keys():
        total_path.insert(0, current)
        current = cameFrom[current]
    return total_path

def compareNodes(a, b):
    if a.i == b.i and a.j == b.j:
        return True
    return False

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
        self.final_n = []

        self.gScore = math.inf
        self.fScore = math.inf

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

    def showRec(self, color):
        height = 500//grid_size
        width = 500//grid_size
        # if self.targets:
        #     color = (255, 0, 0)
        pg.draw.rect(win, color, (self.i*(width),self.j*(height),width,height))

    def show(self, color):
        w = 500//grid_size
        x = self.i * w
        y = self.j * w
        line_w = 3
        if self.top:
            pg.draw.line(win, color, (x, y), (x+w, y),line_w)
        if self.right:
            pg.draw.line(win, color, (x+w, y), (x+w, y+w),line_w)
        if self.bottom:
            pg.draw.line(win, color, (x+w, y+w), (x, y+w),line_w)
        if self.left:
            pg.draw.line(win, color, (x, y+w), (x, y),line_w)

for i in range(grid_size):
    for j in range(grid_size):
        grid[i][j] = node(i, j)

start = grid[0][0]
end = grid[grid_size-1][grid_size-1]
# start.targets = True
# end.targets = True

for i in range(grid_size):
    for j in range(grid_size):
        grid[i][j].addNeighbours()
        grid[i][j].show((0, 0, 0))
pg.display.update()

crashed = False
clock = pg.time.Clock()
stack = [start]
start.visited = True

openSet = [start]
closedSet = []
cameFrom = {}
start.gScore = 0
start.fScore = heuristic(start, end)
flag = True
found = False

while not crashed:
    if not found:
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
            current.final_n.append(chosen)
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
    elif not found:
        flag = False
    if not flag:
        if len(openSet) == 0:
            print('No path')
            flag = True
            continue
        current = None
        low = math.inf
        for spot in openSet:
            if spot.fScore < low:
                low = spot.fScore
                current = spot

        if compareNodes(current, end):
            print('Got Path')
            flag = True
            found = True
        openSet.remove(current)
        closedSet.append(current)
        for n in current.final_n:
            # if n.wall:
            #     continue
            temp_gScore = current.gScore + 1        ##1 is the weight of the connecting edge

            if temp_gScore <= n.gScore:
                cameFrom[n] = current
                n.gScore = temp_gScore
                n.fScore = n.gScore + heuristic(n, end)
                if n not in openSet:
                    openSet.append(n)
        path = reconstruct_path(cameFrom, current)
        # for i in closedSet:
        #     i.showRec((255,255,0))
        # for i in openSet:
        #     i.showRec((0,255,0))
        for i in path:
            i.showRec((0,0,255))

    pg.display.update()
    clock.tick(300)