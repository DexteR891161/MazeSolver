import pygame as pg
import math
import random

grid_size = 50
grid = [[0 for x in range(grid_size)] for x in range(grid_size)] 

pg.init()
win = pg.display.set_mode((500,500))
win.fill((0, 0, 0))

def heuristic(current, end):
	a = current.i-end.i
	b = current.j-end.j
	return math.sqrt(a**2 + b**2)

class node:
	def __init__(self, i, j):
		self.i = i
		self.j = j
		self.neighbours = []
		self.gScore = math.inf
		self.fScore = math.inf
		self.wall = False
		self.targets = False

	def addNeighbours(self):
		if self.i > 0:
			self.neighbours.append(grid[self.i-1][self.j])
		if self.j > 0:
			self.neighbours.append(grid[self.i][self.j-1])
		if self.i < grid_size-1:
			self.neighbours.append(grid[self.i+1][self.j])
		if self.j < grid_size-1:
			self.neighbours.append(grid[self.i][self.j+1])

	def addWalls(self, prob):
		if random.uniform(0, 1) < prob and not self.targets:
			self.wall = True

	def show(self, color):
		height = 500//grid_size
		width = 500//grid_size
		if self.wall:
			color = (0, 0, 0)
		if self.targets:
			color = (255, 0, 0)
		pg.draw.rect(win, color, (self.i*(width),self.j*(height),width,height))

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

for i in range(grid_size):
	for j in range(grid_size):
		grid[i][j] = node(i, j)

start = grid[0][0]
end = grid[grid_size-1][0]
start.targets = True
end.targets = True

for i in range(grid_size):
	for j in range(grid_size):
		grid[i][j].addWalls(0.25)
		grid[i][j].addNeighbours()
		grid[i][j].show((255,255,255))
pg.display.update()
crashed = False

clock = pg.time.Clock()

openSet = [start]
closedSet = []
cameFrom = {}
start.gScore = 0
start.fScore = heuristic(start, end)
flag = False
while not crashed:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			crashed = True
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
		openSet.remove(current)
		closedSet.append(current)
		for n in current.neighbours:
			if n.wall:
				continue
			temp_gScore = current.gScore + 1		##1 is the weight of the connecting edge

			if temp_gScore <= n.gScore:
				cameFrom[n] = current
				n.gScore = temp_gScore
				n.fScore = n.gScore + heuristic(n, end)
				if n not in openSet:
					openSet.append(n)
		path = reconstruct_path(cameFrom, current)
		for i in closedSet:
			i.show((255,255,0))
		for i in openSet:
			i.show((0,255,0))
		for i in path:
			i.show((0,0,255))
		pg.display.update()
		clock.tick(60)
