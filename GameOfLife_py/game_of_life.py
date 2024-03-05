
import pygame


COLORS = {'WHITE': (255, 255, 255),
            'BLACK': (26, 18, 11)}



WIDTH = 700  
WIN = pygame.display.set_mode((WIDTH, WIDTH))


class cell:
    def __init__(self, row, col, state):
        self.row = row
        self.col = col
        self.state = state 
        self.neighbors = []

    def update_neighbors():
        pass

    def update_state():
        pass
    
    def get_position(self):
        return self.row, self.col
    


def make_grid(rows, cols):
    grid = []
    
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            cellobj = cell(i,j,COLORS["WHITE"])
            grid[i].append(cellobj)
    
    return grid



def draw_grid(win, grid):
    rows = len(grid)
    cols = len(grid[0])
    gap = WIDTH // rows

    for i in range(rows):
        for j in range(cols):
            rect = pygame.Rect(j * gap, i * gap, gap, gap)
            pygame.draw.rect(win, grid[i][j].state, rect)
            pygame.draw.rect(win, COLORS['BLACK'], rect, 1)  # Drawing grid lines

            
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y,x = pos

    row = x // gap
    col = y // gap

    return row, col


def main(win, width):
    ROWS, COLS = 100, 100
    grid = make_grid(ROWS, COLS)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # Left mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                cell = grid[row][col]
                cell.state = COLORS['BLACK']  # Change cell state to "alive"

        win.fill(COLORS['WHITE'])
        draw_grid(win, grid)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    WIDTH = 700
    WIN = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.init()
    main(WIN, WIDTH)
