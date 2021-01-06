#Tutorial created by techWithTime youtube Tutorial and NEAT-Python AI 0.92 online documentation

#External libaries used inc NEAT AI 
import pygame
import neat
import time
import os
import random

#Font Import 
pygame.font.init()

#const window size doesn't change  
WIN_WIDTH = 500
WIN_HEIGHT = 800

#Global varible generation counter 
GEN = 0

#Loads the images bird1,2,3 and scales them up 2 times
spriteCostume = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]
#Pipe image
obstacleCostume = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
#Base/Floor image
groundImage = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
#Background image
backgroundPic = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))
#Font styles for generation counter and score of birds 
fontStyleAndSize = pygame.font.SysFont("comicsans", 50)

class Bird:
    # 3 BIRD IMAGES LOADED IN 
    IMGS = spriteCostume
    #Maximum tilt on Sprite
    MAX_ROT_ON_SPRITE = 25
    #How much tilt on each frame
    SPRITE_TILT = 20
    #Shows how long between sprite image changes
    SPRITE_COSTUME_CHANGE = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        #How much sprite is tilted
        self.tilt = 0
        self.movement_counter = 0
        self.vel = 0
        self.height = self.y
        self.costume_chosen = 0
        #Starting image for sprite
        self.img = self.IMGS[0]

    def jump(self):
        #Speed when bird flaps up
        self.vel = -10.5
        #Keep track of which direction the bird is facing sets the tick back to 0 after every jump
        self.movement_counter = 0
        #Coordinates of the sprite 
        self.height = self.y

    
    def move(self):
        #Keeps track of how much moved sinced previous jump  
        self.movement_counter += 1

        #Uses the v value to work out how high the bird jumps creates the arc of the birds jumps 
        d = self.vel*self.movement_counter + 1.5*self.movement_counter**2

        #Bounds to ensure sprite doesn't go to high or to low 
        if d >= 16:
            d = 16

        if d < 0:
            d -= 2

        self.y = self.y + d

        #Keeps track of sprites postition 
        if d < 0 or self.y < self.height + 50:
            ##Esnures sprite doesn't tilt the sprite past the max rotation value 
            if self.tilt < self.MAX_ROT_ON_SPRITE:
                self.tilt = self.MAX_ROT_ON_SPRITE
        else:
            if self.tilt > -90:
                self.tilt -= self.SPRITE_TILT

    def draw(self, win):
        #How many times has an image/sprite has been shown 
        self.costume_chosen += 1

        #Check which image to show based on the image count to show the sprite moving up or down  
        if self.costume_chosen <self.SPRITE_COSTUME_CHANGE:
            self.img = self.IMGS[0]
        elif self.costume_chosen < self.SPRITE_COSTUME_CHANGE*2:
            self.img = self.IMGS[1]
        elif self.costume_chosen < self.SPRITE_COSTUME_CHANGE*3:
            self.img = self.IMGS[2]
        elif self.costume_chosen < self.SPRITE_COSTUME_CHANGE*4:
            self.img = self.IMGS[1]
        elif self.costume_chosen == self.SPRITE_COSTUME_CHANGE*4 + 1:
            self.img = self.IMGS[0]
            self.costume_chosen = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.costume_chosen = self.SPRITE_COSTUME_CHANGE*2
       
       #Rotates image around a point
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        #Rotates image around the center of the screen 
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

#Creation of the pipes 
class Pipe:
    
    GAP = 150 #Size of gap between pipes
    VEL = 5 #Speed of pipe creation

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        #Used to flip the pipe image 
        self.PIPE_TOP = pygame.transform.flip(obstacleCostume, False, True)
        self.PIPE_BOTTOM = obstacleCostume

        self.passed = False
        self.set_height()

    #Sets height of pipe to random 
    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    #speed which x value of pipe appears 
    def move(self):
        self.x -= self.VEL

    #Draws pipe
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    #Method to check if first has collided with pipe
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True

        return False 

#Bottom/Ground class
class Base:
    VEL = 5
    WIDTH = groundImage.get_width()
    IMG = groundImage

    
    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        #Loops the base background around when it goes off the screen
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    #Draws the ground 
    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


#Draws the rendered game screen 
def draw_window(win, birds, pipes, base, score, gen):
    #Background image 
    win.blit(backgroundPic, (0,0))
    #Pipes drawn
    for pipe in pipes:
        pipe.draw(win)
    
    #Text rendering 
    text = fontStyleAndSize.render("Score: "+ str(score), 1, (255,255,255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    text = fontStyleAndSize.render("Generation: "+ str(gen), 1, (255,255,255))
    win.blit(text, (10, 10))

    #Draws birds/sprites 
    base.draw(win) 
    for bird in birds:
        bird.draw(win)
    #Draws everything onto the screen 
    pygame.display.update()


#Takes all our genomes(bird movement varibles) and applys them to the config file
def main(genomes, config):
    global GEN
    GEN += 1 #Increments genration counter 
    nets = []
    ge = []
    
    #bird = Bird(230,350) #For a single bird we are wanting to run mutipul at once 
    birds = [] #list 
    
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230,350))
        g.fitness = 0
        ge.append(g)


    base = Base(730)
    pipes = [Pipe(700)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0
    run = True
    while run: 
        #Runs the loop at 30fps remove to speed up simulation 
        clock.tick(30) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run = False
            break
        
        for x, bird in enumerate(birds):
            bird.move()
            #Every full second bird is alive life is increased by 1 at 30fps clock rate 
            ge[x].fitness += 0.1

            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
            if output[0] > 0.5:
                bird.jump()

        
        #bird.move()
        add_pipe = False
        rem = []
        for pipe in pipes:
            for x, bird in  enumerate(birds):
                if pipe.collide(bird):
                   #removes bird that died early 
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                   
            
                #Removes and adds pipe
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            #Calls pipe spawning methid
            pipe.move()
        
        #If pipe is passed add to the score 
        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(700))

        for r in rem:
            pipes.remove(r)
        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >=730 or bird.y < 0:
                #Removes bird that hits the ground or the top of screen
                birds.pop(x)
                nets.pop(x)
                ge.pop(x) 

        #Draws bottom/ground     
        base.move()
    
        draw_window(win,birds, pipes, base, score, GEN)
    
    


def run(config_path):
    #loads into config headings from neat config file
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation,config_path)

    #Pulls population from config file 
    p = neat.Population(config)

    #Console log/record track
    p.add_reporter(neat.StdOutReporter(True)) #Returns us the neat Data from the AI 
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    #how many generations going to run or how many times main() function is run eg:"50" = 50 times
    winner = p.run(main,50)

#Path to neat config file
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-ai-file.txt")
    run(config_path)
        
    



