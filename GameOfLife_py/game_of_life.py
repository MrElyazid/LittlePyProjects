import pygame
import copy

COLORS = {'WHITE': (255, 255, 255),
            'BLACK': (26, 18, 11)}

ROWS , COLS = 30, 30


WIDTH = 700  
WIN = pygame.display.set_mode((WIDTH, WIDTH))


class cell:
    def __init__(self, row, col, state):
        self.row = row
        self.col = col
        self.state = state 
        self.neighbors = []


    def get_position(self):
            return self.row, self.col
    

    def update_state(self, grid):

        live_neighbors_count = 0

        future_state = 0
         
        neighbors = self.get_neighbors(grid)

        for neighbor in neighbors:
            if neighbor.state == COLORS["BLACK"]:
                live_neighbors_count += 1
           
        # update the state of the cell according to the rules in the game https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
        
        if (live_neighbors_count < 2 and self.state == COLORS['BLACK']): # Any live cell with fewer than two live neighbors dies, as if by underpopulation.
            future_state = COLORS['WHITE']
        elif ((live_neighbors_count == 2 or live_neighbors_count == 3) and self.state == COLORS['BLACK']): # Any live cell with two or three live neighbors lives on to the next generation.
            future_state = COLORS['BLACK']
        elif(live_neighbors_count > 3 and self.state == COLORS['BLACK']): # Any live cell with more than three live neighbors dies, as if by overpopulation.
            future_state = COLORS["WHITE"]
        elif(live_neighbors_count == 3 and self.state == COLORS['WHITE']): # Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
            future_state = COLORS["BLACK"]
    
        return future_state if future_state != 0 else self.state



    def get_neighbors(self, grid):
        neighbors = [] 
        r = self.row
        c = self.col
        for i in range(r-1, r+2):  
            for j in range(c-1, c+2):
                if ((i != r or j != c) and in_grid(i, j)):  # Exclude self
                    neighbors.append(grid[i][j])
        return neighbors



def in_grid(row, col):
    return (0 <= row < ROWS and 0 <= col < COLS)


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

    grid = make_grid(ROWS, COLS)

    animation_running = False


    def start_animation(grid):
        grid2 = copy.deepcopy(grid)
        for i in range(ROWS):
            for j in range(COLS):
                state = grid2[i][j].update_state(grid2)
                grid[i][j].state = state
        

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


            if event.type == pygame.KEYDOWN:     # Check for key down event
                if event.key == pygame.K_SPACE:  # Specifically check if the space bar is pressed
                    animation_running = not animation_running


        if animation_running:
            start_animation(grid)
            pygame.time.wait(50)


        win.fill(COLORS['WHITE'])
        draw_grid(win, grid)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    WIDTH = 700
    WIN = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.init()
    main(WIN, WIDTH)
