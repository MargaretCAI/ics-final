import pygame
import random
import copy
score = 0
width = 720
height = 666
gray = (180,180,180)
black = (0,0,0)
PLAY_TIME = 40
size = [width, height]

WHITE = (255,255,255)

background_image = pygame.image.load("image/jump_bg.png")
last_pressed_time = 100
step = 30
start_image = pygame.image.load("instruction/jump_up.png")
clock = pygame.time.Clock()



def start_up_screen():
    while True:
        pygame.init()
        screen = pygame.display.set_mode(size)
        screen.blit(start_image, (0, 0))
        clock.tick(60)
        pygame.display.update()

        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                break

def draw_score(screen, x, y, score):
    font = pygame.font.Font(None, 36)
    text = font.render("Score = " + str(score), 1, WHITE)
    screen.blit(text, (x, y))


def draw_timer(screen, x, y, time_left):
    font = pygame.font.Font(None, 36)  # Choose the font for the text
    text = font.render("Time Left = " + str(time_left), 1, WHITE)  # Create the text
    screen.blit(text, (x, y))  # Draw the text on the screen

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        self.images = []
        self.images.append(pygame.image.load('image/ball_1.png'))
        self.images.append(pygame.image.load('image/ball_2.png'))
        self.images.append(pygame.image.load('image/ball_2.png'))
        self.images.append(pygame.image.load('image/ball_4.png'))
        self.images.append(pygame.image.load('image/ball_5.png'))
        self.images.append(pygame.image.load('image/ball_6.png'))
        self.images.append(pygame.image.load('image/ball_7.png'))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.change_x = 0
        self.change_y = 0
        self.rect.x = width/2
        self.rect.y = 100

    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        self.calc_grav()
        self.rect.y += self.change_y
        self.rect.x += self.change_x


        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > width:
            self.rect.x = width-50



    def go_left(self):
        self.change_x = -7

    def go_right(self):
        self.change_x = 7

    def stop(self):
        self.change_x = 0

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 0.35

class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height,x,y):
        super().__init__()

        self.image = pygame.Surface([width,height])
        self.r = width
        self.image.fill(gray)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def update(self,player):
        if self.rect.y >height:
            self.kill()

def main():
    pygame.init()
    start_up_screen()
    screen = pygame.display.set_mode(size)
    score = 0

    start_time = pygame.time.get_ticks()
    time_left = pygame.time.get_ticks() - start_time
    time_left = time_left / 1000
    time_left = PLAY_TIME - time_left
    time_left = int(time_left)

    pygame.display.set_caption("Falling_ball")
    done = False
    block_list = pygame.sprite.Group()
    player_list = pygame.sprite.Group()

    player = Player()
    player.update()
    player_list.add(player)

    for i in range(6):
        block = Platform(random.randint(15, 200),10,random.randint(0, width),random.randint(0,height))
        block.update(player)
        block_list.add(block)


    time_last_pressed = PLAY_TIME

    while not done:
        list = pygame.sprite.spritecollide(player, block_list, False)
        if len(list)!= 0:
            player.change_y = 0
            player.rect.bottom = list[0].rect.top


        if player.rect.y > height-10 or player.rect.y < -5:
            return 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.change_x = -6
                if event.key == pygame.K_RIGHT:
                    player.change_x = 6
                if event.key == pygame.K_SPACE:
                    if time_last_pressed - time_left > 2:
                        player.change_y = -15
                        score += 10
                        time_last_pressed = copy.deepcopy(time_left)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.change_x = 0
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.change_x = 0

        if len(block_list) < 5:
            block = Platform(random.randrange(40, 100), 10, random.randint(50, width-50), random.randint(0, height / 3))
            block.update(player)
            block_list.add(block)

        if player.rect.top <= height / 2:
            player.rect.y += abs(player.change_y)
            for plat in block_list:
                plat.rect.y += abs(player.change_y)
                if plat.rect.top >= height:
                    plat.kill()

        time_left = pygame.time.get_ticks() - start_time
        time_left = time_left / 1000
        time_left = PLAY_TIME - time_left
        time_left = int(time_left)
        draw_timer(screen, 50, 450, time_left)

        if (start_time + (PLAY_TIME * 1000) <= pygame.time.get_ticks()):
            if score > 140:
                return 0
            else:
                return 0


        block_list.update(player)
        player_list.update()
        screen.blit(background_image, (0, 0))
        draw_timer(screen, 50, 50, time_left)
        draw_score(screen, 70, 10, score)

        player_list.draw(screen)
        block_list.draw(screen)
        clock.tick(70)

        pygame.display.update()
    pygame.quit()

def quit():
    pygame.quit()


# a = main()
# print(a)





