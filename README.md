# MazeSolver
Backtracking algorithm, A* algorithm

## Maze creation using recursive backtracker
The depth-first search algorithm of maze generation is frequently implemented using backtracking. This can be described with a following recursive routine:
1. Choose the initial cell, mark it as visited and push it to the stack
2. While the stack is not empty
    1. Pop a cell from the stack and make it a current cell
    2. If the current cell has any neighbours which have not been visited
        1. Push the current cell to the stack
        2. Choose one of the unvisited neighbours
        3. Remove the wall between the current cell and the chosen cell
        4. Mark the chosen cell as visited and push it to the stack

I have used A* algorithm to solve the maze. Unlike Dijkstra's algorithm A* searched the optimal path using heuristics which make it more efficiant as it does not visits each and every node of the graph.

### Maze Created :
![Alt text](maze.png)

### Solved Maze :
![Alt text](solved_maze.png)
