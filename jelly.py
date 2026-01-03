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
pygame.display.set_caption("Falling Sand Simulator")

# Element colors
element_colors = {
    0: BLACK,      # Empty
    1: WHITE,      # GOL Alive
    10: (255, 255, 0),  # Sand
    11: (0, 0, 255),    # Water
    12: (255, 0, 0),    # Fire
    13: (128, 128, 128) # Wall
}

# Font
font = pygame.font.SysFont(None, 24)

# Grid settings
cell_size = 10
grid_width = grid_width_pixels // cell_size
grid_height = screen_height // cell_size

# Initialize grid
grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]

# Simulation settings
running_simulation = True  # Always running for real-time physics
clock = pygame.time.Clock()
fps = 60  # Frames per second for simulation
selected_element = 10  # Sand
selected_tab = "Sand"

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

def update_sand():
    new_grid = [row[:] for row in grid]
    for x in range(grid_height - 1, -1, -1):  # Bottom to top
        for y in range(grid_width):
            cell = grid[x][y]
            if cell == 10:  # Sand
                if x + 1 < grid_height and new_grid[x + 1][y] == 0:
                    new_grid[x + 1][y] = 10
                    new_grid[x][y] = 0
                elif x + 1 < grid_height and y - 1 >= 0 and new_grid[x + 1][y - 1] == 0:
                    new_grid[x + 1][y - 1] = 10
                    new_grid[x][y] = 0
                elif x + 1 < grid_height and y + 1 < grid_width and new_grid[x + 1][y + 1] == 0:
                    new_grid[x + 1][y + 1] = 10
                    new_grid[x][y] = 0
            elif cell == 11:  # Water
                moved = False
                if x + 1 < grid_height and new_grid[x + 1][y] == 0:
                    new_grid[x + 1][y] = 11
                    new_grid[x][y] = 0
                    moved = True
                elif x + 1 < grid_height and y - 1 >= 0 and new_grid[x + 1][y - 1] == 0:
                    new_grid[x + 1][y - 1] = 11
                    new_grid[x][y] = 0
                    moved = True
                elif x + 1 < grid_height and y + 1 < grid_width and new_grid[x + 1][y + 1] == 0:
                    new_grid[x + 1][y + 1] = 11
                    new_grid[x][y] = 0
                    moved = True
                if not moved:
                    dirs = [1, -1]
                    random.shuffle(dirs)
                    for dy in dirs:
                        ny = y + dy
                        if 0 <= ny < grid_width and new_grid[x][ny] == 0:
                            new_grid[x][ny] = 11
                            new_grid[x][y] = 0
                            break
            elif cell == 12:  # Fire (simple: move up and disappear)
                if x - 1 >= 0 and new_grid[x - 1][y] == 0:
                    new_grid[x - 1][y] = 12
                    new_grid[x][y] = 0
                else:
                    new_grid[x][y] = 0  # Disappear
            # Wall (13) does nothing
    grid[:] = new_grid

def update_gol():
    new_grid = [row[:] for row in grid]
    for x in range(grid_height):
        for y in range(grid_width):
            count = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    nx, ny = x + i, y + j
                    if 0 <= nx < grid_height and 0 <= ny < grid_width and grid[nx][ny] == 1:
                        count += 1
            if grid[x][y] == 1:
                if count == 2 or count == 3:
                    new_grid[x][y] = 1
                else:
                    new_grid[x][y] = 0
            else:
                if count == 3:
                    new_grid[x][y] = 1
    grid[:] = new_grid

def draw_grid():
    for x in range(grid_height):
        for y in range(grid_width):
            if selected_tab == "GOL":
                color = WHITE if grid[x][y] == 1 else BLACK
            else:
                color = element_colors.get(grid[x][y], BLACK)
            pygame.draw.rect(screen, color, (y * cell_size, x * cell_size, cell_size, cell_size))

def clear_grid():
    global grid
    grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]

def randomize_gol():
    global grid
    grid = [[random.randint(0, 1) for _ in range(grid_width)] for _ in range(grid_height)]

def randomize_sand():
    global grid
    grid = [[random.choice([0, 10, 11, 12, 13]) for _ in range(grid_width)] for _ in range(grid_height)]

def randomize_mix():
    global grid
    grid = [[random.choice([0, 1, 10, 11, 12, 13]) for _ in range(grid_width)] for _ in range(grid_height)]

button_lists = {
    "GOL": [
        ("Alive", lambda: setattr(__import__('__main__'), 'selected_element', 1)),
        ("Dead", lambda: setattr(__import__('__main__'), 'selected_element', 0)),
        ("Clear", clear_grid),
        ("Random", randomize_gol),
        ("+ FPS", lambda: setattr(__import__('__main__'), 'fps', min(fps + 5, 120))),
        ("- FPS", lambda: setattr(__import__('__main__'), 'fps', max(fps - 5, 10)))
    ],
    "Sand": [
        ("Sand", lambda: setattr(__import__('__main__'), 'selected_element', 10)),
        ("Water", lambda: setattr(__import__('__main__'), 'selected_element', 11)),
        ("Fire", lambda: setattr(__import__('__main__'), 'selected_element', 12)),
        ("Wall", lambda: setattr(__import__('__main__'), 'selected_element', 13)),
        ("Erase", lambda: setattr(__import__('__main__'), 'selected_element', 0)),
        ("Clear", clear_grid),
        ("Random", randomize_sand),
        ("+ FPS", lambda: setattr(__import__('__main__'), 'fps', min(fps + 5, 120))),
        ("- FPS", lambda: setattr(__import__('__main__'), 'fps', max(fps - 5, 10)))
    ],
    "Mix": [
        ("Sand", lambda: setattr(__import__('__main__'), 'selected_element', 10)),
        ("Water", lambda: setattr(__import__('__main__'), 'selected_element', 11)),
        ("Fire", lambda: setattr(__import__('__main__'), 'selected_element', 12)),
        ("Wall", lambda: setattr(__import__('__main__'), 'selected_element', 13)),
        ("GOL Alive", lambda: setattr(__import__('__main__'), 'selected_element', 1)),
        ("Erase", lambda: setattr(__import__('__main__'), 'selected_element', 0)),
        ("Clear", clear_grid),
        ("Random", randomize_mix),
        ("+ FPS", lambda: setattr(__import__('__main__'), 'fps', min(fps + 5, 120))),
        ("- FPS", lambda: setattr(__import__('__main__'), 'fps', max(fps - 5, 10)))
    ]
}

# Buttons
buttons = []
button_y = 10
button_height = 30
button_width = 180
button_x = grid_width_pixels + 10

# Tabs
tab_buttons = []
tab_y = 10
tab_height = 30
tab_width = 60
tab_x = grid_width_pixels + 10

def add_tab(label, action):
    global tab_y
    rect = pygame.Rect(tab_x, tab_y, tab_width, tab_height)
    tab_buttons.append({'rect': rect, 'label': label, 'action': action})
    tab_y += 40

def set_tab(tab):
    global selected_tab, buttons, selected_element
    selected_tab = tab
    buttons = []
    button_y = tab_y + 20  # after tabs
    for label, action in button_lists[tab]:
        rect = pygame.Rect(button_x, button_y, button_width, button_height)
        buttons.append({'rect': rect, 'label': label, 'action': action})
        button_y += 40
    # set default selected
    if tab == "GOL":
        selected_element = 1
    else:
        selected_element = 10

add_tab("GOL", lambda: set_tab("GOL"))
add_tab("Sand", lambda: set_tab("Sand"))
add_tab("Mix", lambda: set_tab("Mix"))

# Initialize buttons for default tab
set_tab("Sand")

def draw_ui():
    # Draw panel
    pygame.draw.rect(screen, GRAY, (grid_width_pixels, 0, panel_width, screen_height))
    
    # Draw tabs
    for tab in tab_buttons:
        color = GREEN if selected_tab == tab['label'] else WHITE
        pygame.draw.rect(screen, color, tab['rect'], 2)
        text = font.render(tab['label'], True, WHITE)
        screen.blit(text, (tab['rect'].x + 5, tab['rect'].y + 5))
    
    # Draw buttons
    for button in buttons:
        color = WHITE
        pygame.draw.rect(screen, color, button['rect'], 2)
        text = font.render(button['label'], True, WHITE)
        screen.blit(text, (button['rect'].x + 10, button['rect'].y + 5))
    
    # Draw selected element
    name_map = {0: 'Empty', 1: 'GOL Alive', 10: 'Sand', 11: 'Water', 12: 'Fire', 13: 'Wall'}
    sel_text = font.render(f"Selected: {name_map.get(selected_element, 'Unknown')}", True, WHITE)
    screen.blit(sel_text, (button_x, button_y + 10))
    fps_text = font.render(f"FPS: {fps}", True, WHITE)
    screen.blit(fps_text, (button_x, button_y + 40))

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
                x = my // cell_size
                y = mx // cell_size
                if 0 <= x < grid_height and 0 <= y < grid_width:
                    grid[x][y] = selected_element
            else:  # Click on UI
                for tab in tab_buttons:
                    if tab['rect'].collidepoint(mx, my):
                        tab['action']()
                        break
                for button in buttons:
                    if button['rect'].collidepoint(mx, my):
                        button['action']()
                        break

    if running_simulation:
        if selected_tab == "GOL":
            update_gol()
        elif selected_tab == "Sand":
            update_sand()
        else:  # Mix
            update_sand()
            update_gol()

    pygame.display.set_caption("Falling Sand Simulator")

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