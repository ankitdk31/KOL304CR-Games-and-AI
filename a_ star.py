import pygame
import math
from queue import PriorityQueue

# Window setup
SCREEN_SIZE = 800
WINDOW = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Pathfinding with A* Algorithm")

# Color definitions (slightly different from original)
COLOR_VISITED = (200, 0, 0)        # Dark red
COLOR_FRONTIER = (0, 180, 0)       # Dark green
COLOR_PATH = (150, 0, 150)         # Purple
COLOR_START = (255, 140, 0)        # Dark orange
COLOR_GOAL = (0, 200, 200)         # Cyan
COLOR_BARRIER = (40, 40, 40)       # Dark grey
COLOR_BG = (245, 245, 245)         # Off-white
COLOR_GRID = (160, 160, 160)       # Grey lines

class Node:
    def __init__(self, row, col, size, total_rows):
        self.row = row
        self.col = col
        self.x = row * size
        self.y = col * size
        self.size = size
        self.color = COLOR_BG
        self.neighbors = []
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    # State checks
    def is_closed(self): return self.color == COLOR_VISITED
    def is_open(self): return self.color == COLOR_FRONTIER
    def is_barrier(self): return self.color == COLOR_BARRIER
    def is_start(self): return self.color == COLOR_START
    def is_goal(self): return self.color == COLOR_GOAL

    # State setters
    def reset(self): self.color = COLOR_BG
    def set_closed(self): self.color = COLOR_VISITED
    def set_open(self): self.color = COLOR_FRONTIER
    def set_barrier(self): self.color = COLOR_BARRIER
    def set_start(self): self.color = COLOR_START
    def set_goal(self): self.color = COLOR_GOAL
    def set_path(self): self.color = COLOR_PATH

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))

    def update_neighbors(self, grid):
        self.neighbors.clear()
        # Down
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        # Up
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        # Right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        # Left
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False  # Not used for direct comparison

# Manhattan distance heuristic
def heuristic(a, b):
    x1, y1 = a
    x2, y2 = b
    return abs(x2 - x1) + abs(y2 - y1)

# Reconstructs path
def build_path(origin, current, draw):
    while current in origin:
        current = origin[current]
        current.set_path()
        draw()

# A* Search Implementation
def a_star(draw, grid, start, goal):
    counter = 0
    open_nodes = PriorityQueue()
    open_nodes.put((0, counter, start))
    came_from = {}
    g_cost = {node: float("inf") for row in grid for node in row}
    f_cost = {node: float("inf") for row in grid for node in row}
    g_cost[start] = 0
    f_cost[start] = heuristic(start.get_pos(), goal.get_pos())

    open_set_tracker = {start}

    while not open_nodes.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_nodes.get()[2]
        open_set_tracker.remove(current)

        if current == goal:
            build_path(came_from, goal, draw)
            goal.set_goal()
            return True

        for neighbor in current.neighbors:
            temp_g = g_cost[current] + 1
            if temp_g < g_cost[neighbor]:
                came_from[neighbor] = current
                g_cost[neighbor] = temp_g
                f_cost[neighbor] = temp_g + heuristic(neighbor.get_pos(), goal.get_pos())
                if neighbor not in open_set_tracker:
                    counter += 1
                    open_nodes.put((f_cost[neighbor], counter, neighbor))
                    open_set_tracker.add(neighbor)
                    neighbor.set_open()

        draw()
        if current != start:
            current.set_closed()

    return False

# Grid creation
def create_grid(rows, size):
    grid = []
    gap = size // rows
    for i in range(rows):
        grid.append([Node(i, j, gap, rows) for j in range(rows)])
    return grid

def draw_grid(surface, rows, size):
    gap = size // rows
    for i in range(rows):
        pygame.draw.line(surface, COLOR_GRID, (0, i * gap), (size, i * gap))
    for j in range(rows):
        pygame.draw.line(surface, COLOR_GRID, (j * gap, 0), (j * gap, size))

def render(surface, grid, rows, size):
    surface.fill(COLOR_BG)
    for row in grid:
        for node in row:
            node.draw(surface)
    draw_grid(surface, rows, size)
    pygame.display.update()

def get_cell_clicked(pos, rows, size):
    gap = size // rows
    y, x = pos
    return y // gap, x // gap

def main(surface, size):
    ROWS = 50
    grid = create_grid(ROWS, size)

    start = None
    goal = None

    running = True
    while running:
        render(surface, grid, ROWS, size)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Left mouse: place start, goal, barriers
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_cell_clicked(pos, ROWS, size)
                node = grid[row][col]
                if not start and node != goal:
                    start = node
                    start.set_start()
                elif not goal and node != start:
                    goal = node
                    goal.set_goal()
                elif node != start and node != goal:
                    node.set_barrier()

            # Right mouse: reset node
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_cell_clicked(pos, ROWS, size)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == goal:
                    goal = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and goal:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    a_star(lambda: render(surface, grid, ROWS, size), grid, start, goal)

                if event.key == pygame.K_c:
                    start = None
                    goal = None
                    grid = create_grid(ROWS, size)

    pygame.quit()

main(WINDOW, SCREEN_SIZE)
