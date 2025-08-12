from queue import PriorityQueue

class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.neighbors = []

    def get_pos(self):
        return (self.row, self.col)

    def add_neighbors(self, grid):
        rows, cols = len(grid), len(grid[0])
        if self.row > 0 and grid[self.row - 1][self.col] != "#":  # Up
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.row < rows - 1 and grid[self.row + 1][self.col] != "#":  # Down
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.col > 0 and grid[self.row][self.col - 1] != "#":  # Left
            self.neighbors.append(grid[self.row][self.col - 1])
        if self.col < cols - 1 and grid[self.row][self.col + 1] != "#":  # Right
            self.neighbors.append(grid[self.row][self.col + 1])

# Simple Manhattan heuristic
def heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) + abs(y2 - y1)

# Reconstruct path from end -> start using came_from dict
def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        path.append(current.get_pos())
        current = came_from[current]
    path.append(current.get_pos())  # include the start
    path.reverse()
    return path

# a_star function (works with your Node class)
def a_star(draw, grid, start, end):
    """
    draw: optional callback (can be None) called each iteration
    grid: 2D list where traversable cells are Node objects and walls are "#"
    start: Node object for start
    end: Node object for goal
    """
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}

    # collect only Node objects (skip "#")
    nodes = [cell for row in grid for cell in row if cell != "#"]
    g_score = {n: float("inf") for n in nodes}
    f_score = {n: float("inf") for n in nodes}
    g_score[start] = 0
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            path = reconstruct_path(came_from, end)
            if draw:
                draw()
            print("Path:", path)
            return True

        for neighbor in current.neighbors:
            temp_g = g_score[current] + 1  # uniform cost between adjacent nodes
            if temp_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g
                f_score[neighbor] = temp_g + heuristic(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)

        if draw:
            draw()

    return False

# -------------------------
# Example usage (same layout as you provided)
# -------------------------
def draw_placeholder():
    pass  # no visualization; kept for compatibility with the signature

grid_layout = [
    ["S", ".", ".", ".", "."],
    ["#", "#", ".", "#", "."],
    [".", ".", ".", "#", "."],
    [".", "#", "#", "#", "."],
    [".", ".", ".", ".", "E"],
]

# convert layout to Node objects (walls stay as "#")
grid = [[Node(r, c) if cell != "#" else "#" for c, cell in enumerate(row)] for r, row in enumerate(grid_layout)]

# link neighbours
for row in grid:
    for node in row:
        if node != "#":
            node.add_neighbors(grid)

start = grid[0][0]  # S
end = grid[4][4]    # E

if a_star(draw_placeholder, grid, start, end):
    print("Path found!")
else:
    print("No path available.")
