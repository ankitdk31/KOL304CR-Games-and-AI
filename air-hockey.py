import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Air Hockey AI")

# Colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
BLACK = (0, 0, 0)

# Game objects
PADDLE_RADIUS = 20
PUCK_RADIUS = 15
PADDLE_SPEED = 6
PUCK_SPEED = 5

FPS = 60

class Paddle:
    def __init__(self, x, y, color, is_ai=False):
        self.x = x
        self.y = y
        self.color = color
        self.is_ai = is_ai

    def draw(self):
        pygame.draw.circle(WIN, self.color, (int(self.x), int(self.y)), PADDLE_RADIUS)

    def move(self, dy):
        self.y += dy
        self.y = max(PADDLE_RADIUS, min(HEIGHT - PADDLE_RADIUS, self.y))

    def ai_move(self, puck):
        """
        Simple AI: moves toward the puck's Y position, 
        and predicts where the puck will be if coming towards it.
        """
        # Only track puck if it's on AI's side
        if puck.vx > 0:
            target_y = puck.y
        else:
            target_y = HEIGHT // 2

        if self.y < target_y:
            self.move(PADDLE_SPEED)
        elif self.y > target_y:
            self.move(-PADDLE_SPEED)


class Puck:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.choice([-PUCK_SPEED, PUCK_SPEED])
        self.vy = random.choice([-PUCK_SPEED, PUCK_SPEED])

    def draw(self):
        pygame.draw.circle(WIN, BLACK, (int(self.x), int(self.y)), PUCK_RADIUS)

    def move(self):
        self.x += self.vx
        self.y += self.vy

        # Bounce off top/bottom
        if self.y - PUCK_RADIUS <= 0 or self.y + PUCK_RADIUS >= HEIGHT:
            self.vy *= -1

        # Bounce off paddles
        if (self.x - PUCK_RADIUS <= player.x + PADDLE_RADIUS and 
            abs(self.y - player.y) <= PADDLE_RADIUS) and self.vx < 0:
            self.vx *= -1

        if (self.x + PUCK_RADIUS >= ai.x - PADDLE_RADIUS and 
            abs(self.y - ai.y) <= PADDLE_RADIUS) and self.vx > 0:
            self.vx *= -1

        # Reset if goal scored
        if self.x < 0 or self.x > WIDTH:
            self.__init__(WIDTH // 2, HEIGHT // 2)


# Create objects
player = Paddle(50, HEIGHT // 2, BLUE, is_ai=False)
ai = Paddle(WIDTH - 50, HEIGHT // 2, RED, is_ai=True)
puck = Puck(WIDTH // 2, HEIGHT // 2)

def draw():
    WIN.fill(WHITE)
    player.draw()
    ai.draw()
    puck.draw()
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.move(-PADDLE_SPEED)
        if keys[pygame.K_DOWN]:
            player.move(PADDLE_SPEED)

        # AI movement
        ai.ai_move(puck)

        # Move puck
        puck.move()

        # Draw everything
        draw()

    pygame.quit()

if __name__ == "__main__":
    main()
