import pygame
import random
import math

pygame.init()
pygame.font.init()

width=int(input("Enter the width of the grid:"))
height=int(input("Enter the height of the grid:"))
tile = math.gcd(width,height)
if(tile>32):
    tile=tile//4
W, H = (width-2*tile) // tile, (height-2*tile) // tile
FPS = 2

# Set up display
surface = pygame.display.set_mode((width, height), pygame.RESIZABLE)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
surface.fill(pygame.Color('black'))

# Draw the grid
def draw_grid():
    for x in range(tile, width-tile, tile):
        pygame.draw.line(surface, pygame.Color('dimgray'), (x, tile), (x, height-tile), 2)
    pygame.draw.line(surface, pygame.Color('dimgray'), (width-tile, tile), (width-tile, height-tile), 2)
    for y in range(tile, height-tile, tile):
        pygame.draw.line(surface, pygame.Color('dimgray'), (tile, y), (width-tile, y), 2)
    pygame.draw.line(surface, pygame.Color('dimgray'), (tile, height-tile), (width-tile, height-tile), 2)
    pygame.display.flip()

draw_grid()

generation=1
clicked_squares = []
simulating = False
running = True
initial_grid = [[0 for _ in range(W)] for _ in range(H)]


def generate(num):
    return [(random.randrange(W),random.randrange(H)) for a in range(num)]

# Function to check neighbours
def check_neighbours(grid, x, y):
    neighbours = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
    count = 0

    for dx, dy in neighbours:
        nx, ny = x + dx, y + dy
        if 1 <= nx < W and 1 <= ny < H and grid[ny][nx] == 1:
            count += 1
    return count

# Function to simulate the grid
def simulation(grid):
    new_grid = [[0 for _ in range(W)] for _ in range(H)]
    for y in range(H):
        for x in range(W):
            neighbours = check_neighbours(grid, x, y)
            if grid[y][x] == 1:
                if neighbours == 2 or neighbours == 3:
                    new_grid[y][x] = 1
            elif grid[y][x] == 0:
                if neighbours == 3:
                    new_grid[y][x] = 1
    return new_grid

# Main loop
while running:
    pygame.display.set_caption("Playing" if simulating else "Paused")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and not simulating:
            # shows the generation
            text = font.render('Generation:{}'.format(generation), True, pygame.Color('yellow'))
            surface.blit(text,(0,2))
            pygame.display.flip()
            # initiating simulation using mouse by pressing cells
            mouse_x, mouse_y = event.pos
            grid_x, grid_y = mouse_x // tile, mouse_y // tile
            if (grid_x, grid_y) not in clicked_squares:
                clicked_squares.append((grid_x, grid_y))
                initial_grid[grid_y][grid_x] = 1
                pygame.draw.rect(surface, pygame.Color('green'), (grid_x * tile, grid_y * tile, tile, tile))
                pygame.display.flip()

        elif event.type == pygame.KEYDOWN:

            # Starts and pauses the simulation
            if event.key == pygame.K_SPACE:
                simulating = not simulating

            # provides you a random configuration
            if event.key == pygame.K_g:
                surface.fill(pygame.Color('black'))
                draw_grid()
                text = font.render('Generation:{}'.format(generation), True, pygame.Color('yellow'))
                surface.blit(text,(0,2))
                init_grid=generate(random.randrange(4,12)*tile)
                for x,y in init_grid:
                    if 1<=x<W and 1<=y<H:
                        initial_grid[y][x]=1
                        pygame.draw.rect(surface, pygame.Color('green'), (x* tile, y* tile, tile, tile))
                pygame.display.flip()

            # Resets the game
            if event.key ==pygame.K_c:
                surface.fill(pygame.Color('black'))
                draw_grid()
                generation=1
                initial_grid = [[0 for _ in range(W)] for _ in range(H)]
                simulating=False

    if simulating:
        surface.fill(pygame.Color('black'))
        print("Initial Grid before Simulation:")
        for row in initial_grid:
            print(row)  # Print the initial grid before updating it
        initial_grid = simulation(initial_grid)
        print("Initial Grid after Simulation:")
        for row in initial_grid:
            print(row)  # Print the initial grid after updating it
        draw_grid()
        
        text = font.render('Generation:{}'.format(generation), True, pygame.Color('yellow'))
        surface.blit(text,(0,2))
        clicked_squares = [(x, y) for y in range(H) for x in range(W) if initial_grid[y][x] == 1]
        for grid_x, grid_y in clicked_squares:
            pygame.draw.rect(surface, pygame.Color('green'), (grid_x * tile, grid_y * tile, tile, tile))
        generation+=1
        pygame.display.flip()
        clock.tick(FPS)

    pygame.display.flip()

pygame.quit()
