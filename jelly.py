import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Conway's Game of Life")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Grid settings
cell_size = 10
grid_width = screen_width // cell_size
grid_height = screen_height // cell_size

# Initialize grid
grid = [[False for _ in range(grid_width)] for _ in range(grid_height)]

# Simulation settings
running_simulation = False
clock = pygame.time.Clock()
fps = 10  # Frames per second for simulation

def count_neighbors(x, y):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            nx, ny = x + i, y + j
            if 0 <= nx < grid_height and 0 <= ny < grid_width:
                if grid[nx][ny]:
                    count += 1
    return count

def update_grid():
    new_grid = [[False for _ in range(grid_width)] for _ in range(grid_height)]
    for x in range(grid_height):
        for y in range(grid_width):
            neighbors = count_neighbors(x, y)
            if grid[x][y]:
                if neighbors == 2 or neighbors == 3:
                    new_grid[x][y] = True
            else:
                if neighbors == 3:
                    new_grid[x][y] = True
    return new_grid

def draw_grid():
    for x in range(grid_height):
        for y in range(grid_width):
            color = WHITE if grid[x][y] else BLACK
            pygame.draw.rect(screen, color, (y * cell_size, x * cell_size, cell_size, cell_size))

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not running_simulation:
                mx, my = pygame.mouse.get_pos()
                x = my // cell_size
                y = mx // cell_size
                if 0 <= x < grid_height and 0 <= y < grid_width:
                    grid[x][y] = not grid[x][y]
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running_simulation = not running_simulation
            elif event.key == pygame.K_r:
                grid = [[random.choice([True, False]) for _ in range(grid_width)] for _ in range(grid_height)]
            elif event.key == pygame.K_c:
                grid = [[False for _ in range(grid_width)] for _ in range(grid_height)]

    if running_simulation:
        grid = update_grid()

    # Fill the screen with black
    screen.fill(BLACK)
    
    if running_simulation:
        print("Simulation running...")

    # Draw the grid
    draw_grid()
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(fps)

# Quit Pygame
pygame.quit()