import pygame
import random


# assets : 
ROCK = pygame.image.load("rock_paper_scissors_war\\assets\\rock.png")
SCISSOR = pygame.image.load("rock_paper_scissors_war\\assets\scissors.png")
PAPER = pygame.image.load("rock_paper_scissors_war\\assets\paper.png")



IMG_SIZE = 50



class object:

    def get_pos():
        # returns the position of an object ( rock, paper or scissor )
        pass


    def __init__(self, x, y, nature):
        self.x = x
        self.y = y
        self.nature = nature
        self.image = self.get_image()



    def get_image(self):
        
        if self.nature == 'rock':
            return pygame.transform.scale(ROCK, (IMG_SIZE, IMG_SIZE))
        elif self.nature == 'paper':
            return pygame.transform.scale(PAPER, (IMG_SIZE, IMG_SIZE))
        elif self.nature == 'scissor':
            return pygame.transform.scale(SCISSOR, (IMG_SIZE, IMG_SIZE))



    def update(self):
        # update the nature of the object according to rps rules, also responsible for the objects movement
        pass


    def draw(self, window):
        window.blit(self.image, (self.x, self.y))


def spawn_objects(n):
    objects = []

    for _ in range(n):
        x = random.randint(0, WIDTH-IMG_SIZE)
        y = random.randint(0, HEIGHT-IMG_SIZE)
        nature = random.choice(['rock', 'paper', 'scissor'])
        objects.append(object(x, y, nature))






def main(WIDTH, HEIGHT):
    run = True

    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

    clock = pygame.time.Clock()
    objects = spawn_objects(50)


    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for obj in objects:
            obj.update(objects)

        WINDOW.fill((255, 255, 255))

        for obj in objects:
            obj.draw(WINDOW)

        pygame.display.update()

        clock.tick(60)



if __name__ == "__main__":
    WIDTH = 700
    HEIGHT = 600
    pygame.init()
    main(WIDTH, HEIGHT)