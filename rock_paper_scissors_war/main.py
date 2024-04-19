import pygame
import random


ROCK = pygame.image.load("assets/rock.png")
SCISSOR = pygame.image.load("assets/scissors.png")
PAPER = pygame.image.load("assets/paper.png")


IMG_SIZE = 50


# rules of the game ( in reverse to change the defeated game item easily with dictionary values )
BEATS = {
    'scissor': 'rock',   
    'paper': 'scissor',  
    'rock': 'paper'     
}

class GameItem:
    def __init__(self, x, y, nature):
        self.x = x
        self.y = y
        self.nature = nature
        self.image = self.get_image(nature)
        self.rect = pygame.Rect(x, y, IMG_SIZE, IMG_SIZE)
        self.dx = random.choice([-2, 2, -1, 1])  
        self.dy = random.choice([-2, 2, -1, 1])  # THIS WAS THE BUG FOR NON MOVING GAMEITEMS !!!! choice >>> randint

    def get_image(self, nature):
        if nature == 'rock':
            return pygame.transform.scale(ROCK, (IMG_SIZE, IMG_SIZE))
        elif nature == 'paper':
            return pygame.transform.scale(PAPER, (IMG_SIZE, IMG_SIZE))
        elif nature == 'scissor':
            return pygame.transform.scale(SCISSOR, (IMG_SIZE, IMG_SIZE))

    def update(self, width, height, objects):

        self.x += self.dx
        self.y += self.dy
        self.rect.move_ip(self.dx, self.dy)


        if self.x < 0 or self.x > width - IMG_SIZE:
            self.dx = -self.dx
        if self.y < 0 or self.y > height - IMG_SIZE:
            self.dy = -self.dy


        for obj in objects:
            if obj != self and self.rect.colliderect(obj.rect):
                if BEATS[self.nature] == obj.nature:
                    self.change_nature(obj.nature)

    def change_nature(self, new_nature):
        self.nature = new_nature
        self.image = self.get_image(new_nature)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

def spawn_objects(n, width, height):
    objects = []
    for i in range(n):
        x = random.randint(0, width - IMG_SIZE)
        y = random.randint(0, height - IMG_SIZE)


        # this portion is to spawn the same number of GmeItems
       
        # if i % 3 == 0:
        #     objects.append(GameItem(x, y, 'rock'))
        # elif i % 3 == 2:
        #     objects.append(GameItem(x, y, 'paper'))
        # elif i % 3 == 1:
        #     objects.append(GameItem(x, y, 'scissor'))

            
        nature = random.choice(['rock', 'paper', 'scissor'])
        objects.append(GameItem(x, y, nature))


    return objects

def main(WIDTH, HEIGHT):
    pygame.init()
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    objects = spawn_objects(30, WIDTH, HEIGHT)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for obj in objects:
            obj.update(WIDTH, HEIGHT, objects)

        WINDOW.fill((255, 255, 255))  

        for obj in objects:
            obj.draw(WINDOW)

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    WIDTH = 700
    HEIGHT = 600
    main(WIDTH, HEIGHT)
