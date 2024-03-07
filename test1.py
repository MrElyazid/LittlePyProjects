import pygame
import copy



COLORS = {
    'WHITE': (255, 255, 255),
    'BLACK': (26, 18, 11)
}

ROWS, COLS = 30, 30

WIDTH = 700
WIN = pygame.display.set_mode((WIDTH, WIDTH))


class Cell:  # Capitalized class name
    def __init__(self, row, col, state):
        self.row = row
        self.col = col
        self.state = state
        self.neighbors = []

    def get_position(self):
        return self.row, self.col

    def update_state(self, grid):
        live_neighbors_count = 0
        neighbors = self.get_neighbors(grid)

        for neighbor in neighbors:
            if neighbor.state == COLORS["WHITE"]:
                live_neighbors_count += 1

        # Correct the conditional logic and indentation
        if self.state == COLORS['BLACK']:
            if live_neighbors_count < 2 or live_neighbors_count > 3:  # Underpopulation or overpopulation
                self.state = COLORS['WHITE']
        elif self.state == COLORS['WHITE'] and live_neighbors_count == 3:  # Reproduction
            self.state = COLORS['BLACK']

    def get_neighbors(self, grid):
        neighbors = []
        r = self.row
        c = self.col
        for i in range(r - 1, r + 2):  # Include r and c in the range for 8 neighbors
            for j in range(c - 1, c + 2):
                if (0 <= i < ROWS and 0 <= j < COLS) and (i != r or j != c):  # Check if within grid and not itself
                    neighbors.append(grid[i][j])
        return neighbors




def make_grid(rows, cols):
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            cellobj = Cell(i, j, COLORS["WHITE"])
            grid[i].append(cellobj)
    return grid


def draw_grid(win, grid):
    rows = len(grid)
    cols = len(grid[0])
    gap = WIDTH // rows

    for i in range(rows):
        for j in range(cols):
            rect = pygame.Rect(j * gap, i * gap, gap, gap)
            pygame.draw.rect(win, COLORS['WHITE'], rect)
            pygame.draw.rect(win, COLORS['BLACK'], rect, 1)  # Drawing grid lines


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = x // gap
    col = y // gap

    return row, col


def main(win, width):
    grid = make_grid(ROWS, COLS)

    def start_animation(grid):
        grid2 = copy.deepcopy(grid)
        for i in range(ROWS):
            for j in range(COLS):
                grid2[i][j].update_state(grid)

        grid = copy.deepcopy(grid2)

        

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # Left mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                grid[row][col].state = COLORS['BLACK']  # Change cell state to "alive"

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:  # Check if the space bar is pressed
                start_animation(grid)

        win.fill(COLORS['WHITE'])
        draw_grid(win, grid)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    WIDTH = 700
    WIN = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.init()
    main(WIN, WIDTH)
