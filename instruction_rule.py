import pygame
import random
clock = pygame.time.Clock()
beta = 255
blue = (0,0,255)

def title_loop(filename):
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    image = pygame.image.load(filename)
    done = False
    alpha = 255
    while not done:
        alpha = max(alpha-2,0)
        if alpha == 1:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 1
        screen.fill((0, 0, 0))
        image.set_alpha(alpha)
        clock.tick(60)
        screen.blit(image, (0, 0))
        pygame.display.update()



class Simulation:
    def __init__(self, num_stars, max_depth):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.num_stars = num_stars
        self.max_depth = max_depth
        self.init_stars()

    def init_stars(self):
        self.stars = []
        for i in range(self.num_stars):
            star = [random.randrange(-25,25), random.randrange(-25,25), random.randrange(1, self.max_depth)]
            self.stars.append(star)

    def move_and_draw_stars(self):
        origin_x = self.screen.get_width() / 2
        origin_y = self.screen.get_height() / 2

        for star in self.stars:

            star[2] -= 0.19

            if star[2] <= 0:
                star[0] = random.randrange(-25,25)
                star[1] = random.randrange(-25,25)
                star[2] = self.max_depth

            k = 128.0 / star[2]
            x = int(star[0] * k + origin_x)
            y = int(star[1] * k + origin_y)

            if 0 <= x < self.screen.get_width() and 0 <= y < self.screen.get_height():
                size = (1 - float(star[2]) / self.max_depth) * 5
                shade = (1 - float(star[2]) / self.max_depth) * 255
                self.screen.fill((shade,shade,shade),(x,y,size,size))

    def run(self):
        while 1:
            global beta
            beta = max(beta - 2, 0)
            if beta == 1:
                break
            self.clock.tick(50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            self.screen.fill((30,30,30))
            self.move_and_draw_stars()
            pygame.display.flip()


def main():
    pygame.init()
    font = pygame.font.Font(None, 70)
    black = (0,0,0)
    alpha = 255
    state = 1


    while True:
        screen = pygame.display.set_mode((640, 480))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        if state == 1:
            orig_surf = font.render("Welcome to super 8+1", True, black)
            txt_surf = orig_surf.copy()
            alpha_surf = pygame.Surface(txt_surf.get_size(), pygame.SRCALPHA)
            if alpha > 0:
                alpha = max(alpha - 2, 0)
                txt_surf = orig_surf.copy()
                alpha_surf.fill((255, 255, 255, alpha))
                txt_surf.blit(alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                if alpha == 1:
                    alpha = 255
                    state = 2
            screen.fill((255, 255, 255))
            screen.blit(txt_surf, (50, 230))
            pygame.display.flip()
            clock.tick(30)


        if state == 2:
            title_loop("image/win_1.png")
            state = 3

        if state == 3:
            title_loop("image/win_2.png")
            state = 4

        if state == 4:
            title_loop("image/win_3.png")
            state = 5

        if state == 5:
            title_loop("image/win_4.png")
            state = 6

        if state == 6:
            title_loop("image/win_5.png")
            state = 7

        if state == 7:
            title_loop("image/win_6.png")
            state = 8

        if state == 8:
            Simulation(512, 32).run()
            state = 9

        if state == 9:
            title_loop("image/win_7.png")
            state = 10

        if state == 10:
            title_loop("image/galaxy.png")
            state = 11


        if state == 11:
            title_loop("image/win_9.png")
            state = 12

        if state == 12:
            title_loop("image/win_10.png")
            state = 13

        if state == 13:
            orig_surf = font.render("Good Luck!", True, black)
            txt_surf = orig_surf.copy()
            alpha_surf = pygame.Surface(txt_surf.get_size(), pygame.SRCALPHA)
            if alpha > 0:
                alpha = max(alpha - 2, 0)
                txt_surf = orig_surf.copy()
                alpha_surf.fill((255, 255, 255, alpha))
                txt_surf.blit(alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                if alpha == 1:
                    alpha = 255
                    state = 14
            screen.fill((255, 255, 255))
            screen.blit(txt_surf, (140, 200))
            pygame.display.flip()
            clock.tick(30)

        if state == 14:
            pygame.quit()


def quit():
    pygame.quit()


if __name__ == '__main__':
    main()









