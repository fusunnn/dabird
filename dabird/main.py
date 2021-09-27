import pygame
import random
pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 900, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('daBird')
LG = pygame.mixer.Sound('daBird/Assets/testgo.wav')


FPS = 30
VEL = 5
birdWidth, birdHeight = 70, 50
background_image = pygame.image.load("daBird/Assets/dabg.jpg")
birdSpawn = pygame.transform.scale(pygame.image.load('daBird/Assets/dababy.png'), (birdWidth, birdHeight))
greenBlockImage = pygame.image.load('daBird/Assets/finalbaby.png')
scoreFont = pygame.font.SysFont('comicsans', 50)


class Bird:
    IMG = birdSpawn
    MAX_ANGLE = 25
    ROT_VEL = 20
    ANIMATION_T = 5

    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img = self.IMG
        self.img_count = 0

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        d = self.vel*self.tick_count + 1.5*self.tick_count**2
        if d >= 16:
            d = 16
        if d < 0 :
            d -= 2
        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ANGLE:
                self.tilt = self.MAX_ANGLE
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1

        rotated_img = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_img, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class greenBlocks:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.top_pipe = pygame.transform.flip(greenBlockImage, False, True)
        self.bot_pipe = greenBlockImage
        self.passed = False

        self.set_height()

    def set_height(self):
        self.height = random.randint(50, 250)
        self.top = self.height - self.top_pipe.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.top_pipe, (self.x, self.top))
        win.blit(self.bot_pipe, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.top_pipe)
        bottom_mask = pygame.mask.from_surface(self.bot_pipe)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True

        return False





def generateWindow(win, bird, pipes, score):
    win.blit(background_image, [0, 0])
    bird.draw(win)

    for pipe in pipes:
        pipe.draw(win)

    text = scoreFont.render(f'Score: {str(score)}', 1 , (255,255,255))
    win.blit(text, (WIDTH - 10 - text.get_width(), 10))

    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    run = True
    bird = Bird(300, 250)
    score = 0
    pipes = [greenBlocks(900)]

    while run:
        add_pipe = False
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()


        bird.move()

        absblocks = []
        for i in pipes:
            if i.collide(bird):
                main()
            if i.x + i.top_pipe.get_width() < 0:
                absblocks.append(i)
            if not i.passed and i.x < bird.x:
                i.passed = True
                add_pipe = True
            i.move()
        if add_pipe:
            score += 1
            LG.play(0)
            pipes.append(greenBlocks(900))
        for a in absblocks:
            pipes.remove(a)

        if bird.y + bird.img.get_height() >= 500:
            main()

        generateWindow(win, bird, pipes, score)



    pygame.quit()
    quit()

main()
