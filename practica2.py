import pygame
import numpy as np
import sys

# Initialize pygame
pygame.init()

# Get the screen dimensions for maximized window mode
screen_info = pygame.display.Info()
WIDTH, HEIGHT = screen_info.current_w - 100, screen_info.current_h - 100  # Leave some margin
INITIAL_CELL_SIZE = 5
MIN_CELL_SIZE = 1
MAX_CELL_SIZE = 10
current_cell_size = INITIAL_CELL_SIZE

# Calculate grid dimensions - make it larger to accommodate zooming
GRID_WIDTH = WIDTH * 2 // current_cell_size
GRID_HEIGHT = HEIGHT * 2 // current_cell_size

# Set up the display - maximized window instead of fullscreen
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Rule 30 Cellular Automaton")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Rule 30 function
def apply_rule30(a, b, c):
    pattern = (a << 2) | (b << 1) | c
    # Rule 30: 00011110 in binary (30 in decimal)
    return 1 if pattern in [1, 2, 3, 4] else 0

# Initialize the grid with a single cell in the middle
def initialize_grid():
    # Create a history of states for vertical scrolling
    history = []
    first_row = np.zeros(GRID_WIDTH, dtype=int)
    first_row[GRID_WIDTH // 2] = 1  # Set middle cell to active
    history.append(first_row)
    return history

# Compute the next generation based on Rule 30
def next_generation(current_row):
    next_row = np.zeros_like(current_row)
    for i in range(len(current_row)):
        left = current_row[(i - 1) % len(current_row)]
        center = current_row[i]
        right = current_row[(i + 1) % len(current_row)]
        next_row[i] = apply_rule30(left, center, right)
    return next_row

# Draw the cells on the screen
def draw_cells(history, view_x, view_y, cell_size):
    screen.fill(WHITE)
    
    # Calculate visible cells based on current cell size
    visible_width = WIDTH // cell_size
    visible_height = HEIGHT // cell_size
    
    # Calculate the range of rows and columns to display based on view position
    start_row = max(0, int(view_y / cell_size))
    end_row = min(len(history), start_row + visible_height + 1)
    
    start_col = max(0, int(view_x / cell_size))
    end_col = min(GRID_WIDTH, start_col + visible_width + 1)
    
    for y in range(start_row, end_row):
        if y >= len(history):
            break
        
        row = history[y]
        for x in range(start_col, end_col):
            if x >= len(row):
                break
                
            if row[x] == 1:
                pygame.draw.rect(
                    screen,
                    BLACK,
                    (x * cell_size - view_x, y * cell_size - view_y, cell_size, cell_size)
                )

def main():
    # Initialize the grid
    history = initialize_grid()
    
    # Generate enough generations to fill the screen initially
    for _ in range(GRID_HEIGHT * 2):  # Double the screen height for scrolling
        next_row = next_generation(history[-1])
        history.append(next_row)
    
    # View position for panning
    view_x = 0
    view_y = 0
      # For handling mouse drag and zoom
    dragging = False
    prev_mouse_pos = (0, 0)
    cell_size = INITIAL_CELL_SIZE
    
    # Main game loop
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    dragging = True
                    prev_mouse_pos = event.pos
                elif event.button == 4:  # Mouse wheel scroll up - zoom out
                    # Save the mouse position before zoom for centering
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    
                    # Record world coordinates under mouse before zoom
                    world_x = view_x + mouse_x
                    world_y = view_y + mouse_y
                    
                    # Calculate cell coordinates
                    cell_x = world_x / cell_size
                    cell_y = world_y / cell_size
                    
                    # Zoom out (increase cell size) if not at maximum
                    if cell_size < MAX_CELL_SIZE:
                        cell_size += 1
                    
                    # Adjust view position to keep the same logical cell under the mouse
                    view_x = cell_x * cell_size - mouse_x
                    view_y = cell_y * cell_size - mouse_y
                    
                elif event.button == 5:  # Mouse wheel scroll down - zoom in
                    # Save the mouse position before zoom for centering
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    
                    # Record world coordinates under mouse before zoom
                    world_x = view_x + mouse_x
                    world_y = view_y + mouse_y
                    
                    # Calculate cell coordinates
                    cell_x = world_x / cell_size
                    cell_y = world_y / cell_size
                    
                    # Zoom in (decrease cell size) if not at minimum
                    if cell_size > MIN_CELL_SIZE:
                        cell_size -= 1
                    
                    # Adjust view position to keep the same logical cell under the mouse
                    view_x = cell_x * cell_size - mouse_x
                    view_y = cell_y * cell_size - mouse_y
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    # Calculate the movement delta
                    dx = prev_mouse_pos[0] - event.pos[0]
                    dy = prev_mouse_pos[1] - event.pos[1]
                    
                    # Update the view position
                    view_x += dx
                    view_y += dy
                    
                    # Ensure view stays within bounds - adjusted for dynamic cell size
                    max_x = (GRID_WIDTH * cell_size) - WIDTH
                    max_y = (len(history) * cell_size) - HEIGHT
                    view_x = max(0, min(view_x, max_x if max_x > 0 else 0))
                    view_y = max(0, min(view_y, max_y if max_y > 0 else 0))
                    
                    prev_mouse_pos = event.pos
          # Generate new rows if we're approaching the bottom of our history
        # This ensures we always generate more rows as needed - no limit
        if view_y + HEIGHT > (len(history) - GRID_HEIGHT // 2) * cell_size:
            for _ in range(GRID_HEIGHT // 2):
                next_row = next_generation(history[-1])
                history.append(next_row)
        
        # Draw the current state with the current cell size
        draw_cells(history, view_x, view_y, cell_size)
        
        # Update the display
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()