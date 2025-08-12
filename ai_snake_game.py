import pygame
import random
from collections import deque

# Screen setup
WIDTH, HEIGHT = 400, 400
CELL_SIZE = 20
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game AI")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class SnakeGameAI:
    def __init__(self):
        self.reset()

    def reset(self):
        self.snake = deque([(5, 5)])
        self.direction = (1, 0)
        self.spawn_food()
        self.score = 0

    def spawn_food(self):
        while True:
            self.food = (random.randint(0, COLS-1), random.randint(0, ROWS-1))
            if self.food not in self.snake:
                break

    def draw(self):
        WIN.fill(BLACK)
        # Draw snake
        for segment in self.snake:
            pygame.draw.rect(WIN, GREEN, (segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        # Draw food
        pygame.draw.rect(WIN, RED, (self.food[0]*CELL_SIZE, self.food[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.update()

    def bfs_path(self, start, goal):
        """Breadth-First Search to find shortest path to goal."""
        queue = deque([start])
        came_from = {start: None}

        while queue:
            current = queue.popleft()
            if current == goal:
                break

            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                nx, ny = current[0] + dx, current[1] + dy
                if 0 <= nx < COLS and 0 <= ny < ROWS and (nx, ny) not in self.snake and (nx, ny) not in came_from:
                    came_from[(nx, ny)] = current
                    queue.append((nx, ny))

        # Reconstruct path
        if goal not in came_from:
            return None
        path = []
        node = goal
        while node != start:
            path.append(node)
            node = came_from[node]
        path.reverse()
        return path

    def ai_decision(self):
        """AI chooses next move based on BFS path to food."""
        path = self.bfs_path(self.snake[0], self.food)
        if path:
            next_cell = path[0]
            self.direction = (next_cell[0] - self.snake[0][0], next_cell[1] - self.snake[0][1])
        else:
            # No safe path — move randomly to survive
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                nx, ny = self.snake[0][0] + dx, self.snake[0][1] + dy
                if 0 <= nx < COLS and 0 <= ny < ROWS and (nx, ny) not in self.snake:
                    self.direction = (dx, dy)
                    break

    def step(self):
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Check collision
        if (new_head in self.snake) or not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS):
            return False  # Game over

        self.snake.appendleft(new_head)

        # Check food
        if new_head == self.food:
            self.score += 1
            self.spawn_food()
        else:
            self.snake.pop()

        return True

def main():
    clock = pygame.time.Clock()
    game = SnakeGameAI()
    run = True

    while run:
        clock.tick(10)  # AI speed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        game.ai_decision()
        if not game.step():
            print(f"Game over! Score: {game.score}")
            game.reset()

        game.draw()

    pygame.quit()

if __name__ == "__main__":
    main()
