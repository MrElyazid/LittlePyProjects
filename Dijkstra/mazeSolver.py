import pygame
import heapq


COLORS = {
    'GREEN': (88, 230, 53),
    'LIGHTBLUE': (60, 174, 240),
    'BLUE': (47, 37, 232),
    'WHITE': (255, 255, 255),
    'BLACK': (26, 18, 11),
    'LIGHTGREY': (219, 230, 222),
    'ORANGE': (209, 83, 29),
    'GREY': (114, 123, 125),
    'PURPLE': (101, 78, 146)
}



class Node:
    
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = COLORS['WHITE']
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
       
        return self.row, self.col

    
    def is_visited(self):
        return self.color == COLORS['GREEN']

    def is_unvisited(self):
        return self.color == COLORS['LIGHTBLUE']

    def is_barrier(self):
        return self.color == COLORS['BLACK']

    def is_start(self):
        return self.color == COLORS['ORANGE']

    def is_end(self):
        return self.color == COLORS['PURPLE']

    def reset(self):
        self.color = COLORS['WHITE']

    def make_start(self):
        self.color = COLORS['ORANGE']

    def make_visited(self):
        self.color = COLORS['GREEN']

    def make_unvisited(self):
        self.color = COLORS['LIGHTBLUE']

    def make_barrier(self):
        self.color = COLORS['BLACK']

    def make_end(self):
        self.color = COLORS['PURPLE']

    def make_path(self):
        self.color = COLORS['LIGHTGREY']

    def draw(self, win):
        
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        
        self.neighbors = []

        
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        # Less than method for priority queue, not used but required by heapq
        return False



def final_path(came_from, current, draw):
    # Backtracks from the end node to start node to draw the final path
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def heuristic(p1, p2):
    """Calculate the Euclidean distance between two points"""
    x1, y1 = p1
    x2, y2 = p2
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5



def a_star(draw, grid, start, end):
    count = 0
    open_set = []
    heapq.heappush(open_set, (0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not len(open_set) == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)

        if current == end:
            final_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    heapq.heappush(open_set, (f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_unvisited()

        draw()

        if current != start:
            current.make_visited()

    return False


def dijkstra(draw, grid, start, end):
   
    pq = [[0, start]]
    dist = {node: float("inf") for row in grid for node in row}
    dist[start] = 0
    came_from = {}

    while pq:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        d, current = heapq.heappop(pq)

        if current == end:
            final_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            new_dist = dist[current] + 1  # each edge has a weight of 1
            if new_dist < dist[neighbor]:
                came_from[neighbor] = current
                dist[neighbor] = new_dist
                heapq.heappush(pq, [new_dist, neighbor])
                neighbor.make_unvisited()

        draw()

        if current != start:
            current.make_visited()

    return False

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, COLORS['GREY'], (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, COLORS['GREY'], (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(COLORS['WHITE'])

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def main(win, width, rows):
    grid = make_grid(rows, width)


    start = None
    end = None
    run = True
    while run:

        clock.tick(VISUALIZATION_SPEED)
        draw(win, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != end and node != start:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    if algorithm_choice == 'A':
                        a_star(lambda: draw(win, grid, rows, width), grid, start, end)
                    elif algorithm_choice == 'D':
                        dijkstra(lambda: draw(win, grid, rows, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(rows, width)

    pygame.quit()


if __name__ == "__main__":
    
    user_rows = input("Enter grid size (e.g., 50 for a 50x50 grid): ")
    user_speed = input("Enter visualization speed (1-60, where 60 is fastest): ")
    algorithm_choice = input("Choose algorithm: A for A*, D for Dijkstra: ").strip().upper()
    ROWS = int(user_rows)
    VISUALIZATION_SPEED = int(user_speed)
    WIDTH = 700  
    WIN = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Dijkstra Path Finding Algorithm")
    
    
    clock = pygame.time.Clock()

    main(WIN, WIDTH, ROWS)
