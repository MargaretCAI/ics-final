import random
import pygame


def start_up_screen():
    WIDTH = 800
    HEIGHT = 650
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    clock = pygame.time.Clock()
    start_image = pygame.image.load("instruction/hit_rock_ins.png")
    while True:

        screen.blit(start_image, (0, 0))
        clock.tick(60)
        pygame.display.update()

        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                break


def draw_timer(screen, x, y, time_left):
    font = pygame.font.Font(None, 35)  # Choose the font for the text
    text = font.render("Time Left = " + str(time_left), 1, (0,0,0))  # Create the text
    screen.blit(text, (x, y))



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("image/shooter/playerShip.png")
        self.rect = self.image.get_rect()
        self.speedx = 0

    def update(self):
        HEIGHT = 650
        WIDTH = 800
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]+50
        self.rect.y = HEIGHT-60
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        elif keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        self.rect.x += self.speedx


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image= pygame.image.load("image/shooter/laserRed16.png")
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top < 0:
            self.kill()



class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image/shooter/shield_gold.png.png")
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        HEIGHT = 650
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


class Block(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        WIDTH = 800
        meteor_images = ["image/shooter/big1.png", "image/shooter/big2.png", "image/shooter/med1.png",
                         "image/shooter/med3.png",
                         "image/shooter/small1.png", "image/shooter/small2.png"]
        img = random.choice(meteor_images)
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(5, 20)
        self.speedx = random.randrange(-3, 3)
        self.rotation = 0
        self.rotation_speed = random.randrange(-8, 8)




    def update(self):
        HEIGHT = 650
        WIDTH = 800
        self.rect.x += self.speedx
        self.rect.y += self.speedy



        if (self.rect.top > HEIGHT + 10) or (self.rect.left < -25) or (self.rect.right > WIDTH + 20):
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


def main():
    WHITE = (255, 255, 255)
    black = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    WIDTH = 800
    HEIGHT = 650
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])



    PLAY_TIME = 40
    pygame.init()

    start_up_screen()
    done = False

    screen.fill(WHITE)
    block_list = pygame.sprite.Group()
    bullet_list = pygame.sprite.Group()
    player_list = pygame.sprite.Group()

    for i in range(2):
        block = Block()
        block.rect.x = random.randrange(WIDTH)
        block.rect.y = 0
        block_list.add(block)

    player = Player()
    player_list.add(player)

    score = 0
    start_time = pygame.time.get_ticks()

    while not done:


        time_left = pygame.time.get_ticks() - start_time
        time_left = time_left / 1000
        time_left = PLAY_TIME - time_left
        time_left = int(time_left)
        draw_timer(screen, 50, 450, time_left)

        if (start_time + (PLAY_TIME * 1000) <= pygame.time.get_ticks()):
            return 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 1

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.x+30,player.rect.y+30)
                    bullet_list.add(bullet)

        if len(block_list) < 5:
            for i in range(3):
                block = Block()
                block.rect.x = random.randrange(WIDTH)
                block.rect.y = 0
                block_list.add(block)
            else:
                pass

        block_list.update()
        bullet_list.update()
        player_list.update()

        # Calculate mechanics for each bullet
        for bullet in bullet_list:
            block_hit_list = pygame.sprite.spritecollide(bullet, block_list, True)
            score += 1

        for block in block_list:
            if block.rect.y > HEIGHT:
                block_list.remove(block)

        for block in block_list:
            hit = pygame.sprite.spritecollide(player, block_list, True)
            if hit:
                return 1

        screen.fill(WHITE)
        block_list.draw(screen)
        player_list.draw(screen)
        bullet_list.draw(screen)
        draw_timer(screen, 10, 30, time_left)
        pygame.display.update()
        clock.tick(60)

    pygame.quit()


def quit():
    pygame.quit()





