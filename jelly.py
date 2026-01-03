import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 1000
screen_height = 600
panel_width = 200
grid_width_pixels = screen_width - panel_width
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Conway's Game of Life")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Font
font = pygame.font.SysFont(None, 24)

# Grid settings
cell_size = 10
grid_width = grid_width_pixels // cell_size
grid_height = screen_height // cell_size

# Initialize grid
grid = [[False for _ in range(grid_width)] for _ in range(grid_height)]

# Add a simple starting pattern (glider)
grid[10][10] = True
grid[11][11] = True
grid[11][12] = True
grid[10][12] = True
grid[9][12] = True

# Simulation settings
running_simulation = False
clock = pygame.time.Clock()
fps = 10  # Frames per second for simulation
generation = 0

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
    global generation
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
    generation += 1
    return new_grid

def draw_grid():
    for x in range(grid_height):
        for y in range(grid_width):
            color = WHITE if grid[x][y] else BLACK
            pygame.draw.rect(screen, color, (y * cell_size, x * cell_size, cell_size, cell_size))

def clear_grid():
    global grid, generation
    grid = [[False for _ in range(grid_width)] for _ in range(grid_height)]
    generation = 0

def randomize_grid():
    global grid, generation
    grid = [[random.choice([True, False]) for _ in range(grid_width)] for _ in range(grid_height)]
    generation = 0

def set_pattern(pattern):
    global grid
    clear_grid()
    for px, py in pattern:
        if 0 <= px < grid_height and 0 <= py < grid_width:
            grid[px][py] = True

# Patterns
glider = [(0,1), (1,2), (1,0), (2,1), (2,2)]
blinker = [(0,0), (0,1), (0,2)]
gosper_gun = [
    (5,1), (5,2), (6,1), (6,2), (5,11), (6,11), (7,11), (4,12), (3,13), (3,14), (8,12), (9,13), (9,14),
    (6,15), (4,16), (5,17), (6,17), (6,18), (7,17), (3,21), (4,21), (5,21), (3,22), (4,22), (5,22),
    (2,23), (6,23), (1,25), (2,25), (6,25), (7,25), (3,35), (4,35), (3,36), (4,36)
]

# Buttons
buttons = []
button_y = 10
button_height = 30
button_width = 180
button_x = grid_width_pixels + 10

def add_button(label, action):
    global button_y
    rect = pygame.Rect(button_x, button_y, button_width, button_height)
    buttons.append({'rect': rect, 'label': label, 'action': action})
    button_y += 40

add_button("Play/Pause", lambda: setattr(__import__('__main__'), 'running_simulation', not running_simulation))
add_button("Step", lambda: setattr(__import__('__main__'), 'grid', update_grid()) if not running_simulation else None)
add_button("Clear", clear_grid)
add_button("Random", randomize_grid)
add_button("Glider", lambda: set_pattern([(x+10, y+10) for x,y in glider]))
add_button("Blinker", lambda: set_pattern([(x+10, y+10) for x,y in blinker]))
add_button("Gosper Gun", lambda: set_pattern([(x+10, y+10) for x,y in gosper_gun]))
add_button("+ FPS", lambda: setattr(__import__('__main__'), 'fps', min(fps + 1, 60)))
add_button("- FPS", lambda: setattr(__import__('__main__'), 'fps', max(fps - 1, 1)))

def draw_ui():
    # Draw panel
    pygame.draw.rect(screen, GRAY, (grid_width_pixels, 0, panel_width, screen_height))
    
    # Draw buttons
    for button in buttons:
        color = GREEN if running_simulation and button['label'] == "Play/Pause" else WHITE
        pygame.draw.rect(screen, color, button['rect'], 2)
        text = font.render(button['label'], True, WHITE)
        screen.blit(text, (button['rect'].x + 10, button['rect'].y + 5))
    
    # Draw FPS and Generation
    fps_text = font.render(f"FPS: {fps}", True, WHITE)
    screen.blit(fps_text, (button_x, button_y + 10))
    gen_text = font.render(f"Gen: {generation}", True, WHITE)
    screen.blit(gen_text, (button_x, button_y + 40))

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if mx < grid_width_pixels:  # Click on grid
                if not running_simulation:
                    x = my // cell_size
                    y = mx // cell_size
                    if 0 <= x < grid_height and 0 <= y < grid_width:
                        grid[x][y] = not grid[x][y]
            else:  # Click on UI
                for button in buttons:
                    if button['rect'].collidepoint(mx, my):
                        button['action']()

    if running_simulation:
        grid = update_grid()
        pygame.display.set_caption("Conway's Game of Life - Running")
    else:
        pygame.display.set_caption("Conway's Game of Life - Paused")

    # Fill the screen with black
    screen.fill(BLACK)
    
    # Draw the grid
    draw_grid()
    
    # Draw UI
    draw_ui()
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(fps)

# Quit Pygame
pygame.quit()