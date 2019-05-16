import pygame
import random


width = 700
height = 500

# pygame.display.set_caption("Game_fight")
clock = pygame.time.Clock()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WINNING_SCORE = 70
PLAY_TIME = 30
PLAYER_SPEED = 20
AI_SPEED = 5
BALL_SPEED = 7
size = 15
start_image = pygame.image.load("instruction/catch_ball_ins.png")



def start_up_screen():
    pygame.init()

    while True:
        screen = pygame.display.set_mode((width, height))
        screen.blit(start_image, (0, 0))
        clock.tick(60)
        pygame.display.update()

        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                break

def draw_timer(surface, x, y, time_left):
    font = pygame.font.Font(None, 36)  # Choose the font for the text
    text = font.render("Time Left = " + str(time_left), 1, WHITE)  # Create the text
    surface.blit(text, (x, y))  # Draw the text on the screen

def draw_score(screen, x, y, score):
    font = pygame.font.Font(None, 36)
    text = font.render("Score = " + str(score), 1, WHITE)
    screen.blit(text, (x, y))

def draw_ball(screen, x, y):
    pygame.draw.circle(screen, GREEN, [x, y], size, 0)


def draw_background():
    screen = pygame.display.set_mode((width, height))
    myimage = pygame.image.load("image/11.png")
    imagerect = myimage.get_rect()
    screen.blit(myimage, imagerect)


def draw_stick_figure(screen, x, y, colour, scale):

    pygame.draw.ellipse(screen, BLACK, [int(1 * scale) + x, y, int(10 * scale), int(10 * scale)], 0)

    pygame.draw.line(screen, BLACK, [int(5 * scale) + x, int(17 * scale) + y],
                     [int(10 * scale) + x, int(27 * scale) + y], int(2 * scale))

    pygame.draw.line(screen, BLACK, [int(5 * scale) + x, int(17 * scale) + y], [x, int(27 * scale) + y], int(2 * scale))

    pygame.draw.line(screen, colour, [int(5 * scale) + x, int(17 * scale) + y],
                     [int(5 * scale) + x, int(7 * scale) + y], int(2 * scale))

    pygame.draw.line(screen, colour, [int(5 * scale) + x, int(7 * scale) + y],
                     [int(9 * scale) + x, int(17 * scale) + y], int(2 * scale))
    pygame.draw.line(screen, colour, [int(5 * scale) + x, int(7 * scale) + y],
                     [int(1 * scale) + x, int(17 * scale) + y], int(2 * scale))




def constrainn(num,min,max):
    if num < min:
        num = min
    elif num > max:
        num = max
    return num


def main():

    start_up_screen()

    done = False
    step = 0
    score = 0

    last_score_step = -100

    x_speed = 0
    y_speed = 0

    x_d = 300
    y_coord = 1

    board_x_d = 300
    board_y_coord = 300


    board_moves = (-AI_SPEED, 0, AI_SPEED)
    board_x_direction = 0
    board_y_direction = 0

    ball_x_d = 300
    ball_y_coord = 300



    ball_moves = (-BALL_SPEED, BALL_SPEED)

    ball_x_directon = 0
    ball_y_direction = 0

    start_time = pygame.time.get_ticks()

    while not done:
        screen = pygame.display.set_mode((width, height))
        if score == WINNING_SCORE:
            return 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 1
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    x_speed = -PLAYER_SPEED
                elif event.key == pygame.K_RIGHT:
                    x_speed = PLAYER_SPEED
                elif event.key == pygame.K_UP:
                    y_speed = -PLAYER_SPEED
                elif event.key == pygame.K_DOWN:
                    y_speed = PLAYER_SPEED

            # User let up on a key
            elif event.type == pygame.KEYUP:
                # If it is an arrow key, reset vector back to zero
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_speed = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_speed = 0


        if (start_time + (PLAY_TIME * 1000) <= pygame.time.get_ticks()):
            return 1

        x_d = x_d + x_speed
        y_coord = y_coord + y_speed

        if (step % 30 == 0):
            board_x_direction = random.choice(board_moves)
            board_y_direction = random.choice(board_moves)

        old_board_x_d = board_x_d
        old_board_y_coord = board_y_coord

        board_x_d = board_x_d + board_x_direction
        board_y_coord = board_y_coord + board_y_direction

        board_x_d = constrainn(board_x_d, 0, height)
        board_y_coord = constrainn(board_y_coord, 0, height)

        if (board_x_d == old_board_x_d):
            board_x_direction *= -1
        if (board_y_coord == old_board_y_coord):
            board_y_direction *= -1

        if (step % 20 == 0):
            ball_x_direction = random.choice(ball_moves)
            ball_y_direction = random.choice(ball_moves)

        ball_x_d += ball_x_direction
        ball_y_coord += ball_y_direction

        ball_x_d = constrainn(ball_x_d, 0, width)
        ball_y_coord = constrainn(ball_y_coord, 0, height)

        if (ball_x_d - size <= x_d + 5) and (ball_x_d + size >= x_d - 5) and (
                ball_y_coord - size <= y_coord + 27) and (ball_y_coord + size >= y_coord):
            if (last_score_step + 10 < step):
                score += 10
                ball_x_directon *= -1
                ball_y_direction *= -1
                last_score_step = step

        if y_coord > height:
            y_coord = 0
        if y_coord < 0:
            y_coord = height
        if x_d < 0:
            x_d = width
        if x_d > width:
            x_d = 0






        if (x_d - 5 <= board_x_d + 10) and (x_d + 5 >= board_x_d) and (y_coord - 3 <= board_y_coord + 54) and (
                y_coord + 27 >= board_y_coord):
            return 1


        screen.fill(WHITE)
        draw_background()
        draw_stick_figure(screen, x_d, y_coord, RED, 1)
        draw_stick_figure(screen, board_x_d, board_y_coord, BLUE,
                          2)

        draw_ball(screen, ball_x_d, ball_y_coord)
        draw_score(screen, 550, 450, score)


        time_left = pygame.time.get_ticks() - start_time
        time_left = time_left / 1000
        time_left = PLAY_TIME - time_left
        time_left = int(time_left)

        if time_left < 1:
            return 1
        draw_timer(screen, 50, 450, time_left)

        pygame.display.flip()
        step += 1

        clock.tick(120)
    pygame.quit()


def quit():
    pygame.quit()


