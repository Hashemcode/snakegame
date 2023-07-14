import pygame
import random

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Snake directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)


class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.grow = False

    def update(self):
        head = self.body[0]
        x, y = self.direction
        new_head = (head[0] + x, head[1] + y)

        if new_head in self.body or not self.is_valid_position(new_head):
            return False

        self.body.insert(0, new_head)

        if self.grow:
            self.grow = False
        else:
            self.body.pop()

        return True

    def is_valid_position(self, pos):
        x, y = pos
        return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT

    def change_direction(self, direction):
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def grow_snake(self):
        self.grow = True

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))


class Fruit:
    def __init__(self):
        self.position = self.generate_position()

    def generate_position(self):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in snake.body:
                return x, y

    def draw(self):
        pygame.draw.rect(screen, RED, (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))


snake = Snake()
fruit = Fruit()
eaten_count = 0

running = True
game_over = False

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.change_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.change_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.change_direction(RIGHT)

    if not game_over:
        game_over = not snake.update()

        if snake.body[0] == fruit.position:
            snake.grow_snake()
            fruit.position = fruit.generate_position()
            eaten_count += 1

        snake.draw()
        fruit.draw()

    if game_over:
        restart_text = font.render("Press SPACE to restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(restart_text, restart_rect)

    eaten_text = font.render("Eaten: " + str(eaten_count), True, WHITE)
    screen.blit(eaten_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

    # Restart the game if SPACE key is pressed
    if game_over and pygame.key.get_pressed()[pygame.K_SPACE]:
        snake = Snake()
        fruit = Fruit()
        eaten_count = 0
        game_over = False

pygame.quit()
