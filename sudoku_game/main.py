import pygame
import random

class Cell:
    def __init__(self, value=0, editable=True):
        self.value = value
        self.editable = editable

    def set_value(self, value):
        if self.editable:
            self.value = value

    def get_value(self):
        return self.value


class Square:
    def __init__(self):
        self.cells = [[Cell() for _ in range(3)] for _ in range(3)]

    def get_cell(self, row, col):
        return self.cells[row][col]


class Grid:
    def __init__(self):
        self.squares = [[Square() for _ in range(3)] for _ in range(3)]
        self.initialize_game()

    def get_cell_global(self, row, col):
        square_row, square_col = row // 3, col // 3
        cell_row, cell_col = row % 3, col % 3
        return self.squares[square_row][square_col].get_cell(cell_row, cell_col)

    def initialize_game(self):
        sudoku_grid = generate_sudoku()
        for i in range(9):
            for j in range(9):
                value = sudoku_grid[i][j]
                cell = self.get_cell_global(i, j)
                cell.value = value
                cell.editable = (value == 0)


def get_position(pos, width):
    gap = width // 9
    x, y = pos
    row = y // gap
    col = x // gap
    return (row, col)


def fill_grid(grid):
    find = find_empty_location(grid)
    if not find:
        return True
    else:
        row, col = find

    numbers = list(range(1, 10))
    random.shuffle(numbers)
    for num in numbers:
        if is_valid(grid, num, (row, col)):
            grid[row][col] = num
            if fill_grid(grid):
                return True
            grid[row][col] = 0
    return False

def find_empty_location(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return (i, j)
    return None


def is_valid(grid, num, pos):
    
    row, col = pos
    for i in range(9):
        if grid[row][i] == num or grid[i][col] == num:
            return False
    box_x, box_y = (col // 3) * 3, (row // 3) * 3
    for i in range(box_y, box_y + 3):
        for j in range(box_x, box_x + 3):
            if grid[i][j] == num:
                return False
    return True

def remove_numbers(grid, clues=30):
    attempts = 81 - clues
    while attempts > 0:
        row, col = random.randint(0, 8), random.randint(0, 8)
        while grid[row][col] == 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
        grid[row][col] = 0
        attempts -= 1

def generate_sudoku():
    base_grid = [[0 for _ in range(9)] for _ in range(9)]
    fill_grid(base_grid)
    remove_numbers(base_grid, clues=30)  # Set for medium difficulty
    return base_grid

def main(width, height):
    pygame.init()
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Sudoku")
    clock = pygame.time.Clock()
    grid = Grid()
    selected = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                selected = get_position(pos, width)
            elif event.type == pygame.KEYDOWN:
                if selected and event.unicode.isdigit():
                    digit = int(event.unicode)
                    if 1 <= digit <= 9:
                        row, col = selected
                        cell = grid.get_cell_global(row, col)
                        cell.set_value(digit)

        draw(win, grid, selected, width, height)
        pygame.display.update()
        clock.tick(60)
    pygame.quit()

def draw(win, grid, selected, width, height):
    win.fill((255, 255, 255))
    gap = width // 9
    for i in range(10):
        thick = 4 if i % 3 == 0 else 1
        pygame.draw.line(win, (0, 0, 0), (0, i * gap), (width, i * gap), thick)
        pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, height), thick)

    font = pygame.font.Font(None, 40)
    for i in range(9):
        for j in range(9):
            cell = grid.get_cell_global(i, j)
            value = cell.get_value()
            x, y = j * gap, i * gap
            if value != 0:
                text = font.render(str(value), True, (0, 0, 0))
                win.blit(text, (x + (gap - text.get_width()) / 2, y + (gap - text.get_height()) / 2))
            if selected == (i, j):
                pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)

if __name__ == "__main__":
    WIDTH, HEIGHT = 540, 540  # Smaller window size
    main(WIDTH, HEIGHT)
