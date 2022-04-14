import pygame
import random
pygame.font.init()
pygame.display.set_caption("SNAKE")

WIDTH = 850
HEIGHT = 850

SNAKE_WIDTH = 30
SNAKE_HEIGHT = 30
SNAKE_VELOCITY = 30

APPLE_WIDTH = 30
APPLE_HEIGHT = 30

BORDER_WIDTH = 10
BORDER_HEIGHT = WIDTH

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)

GAME_OVER_FONT = pygame.font.SysFont('comicsans',25)

FPS = 24

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
WINDOW.fill((WHITE))

COLLISION_DEATH = pygame.USEREVENT + 1
COLLISION_EAT = pygame.USEREVENT + 2

score = 0
first_time = True
super_counter = 0
wait_one_cycle = True

def handle_border_collision(snake_head,left_border,right_border,upper_border,lower_border):

    if snake_head.colliderect(left_border):
        pygame.event.post(pygame.event.Event(COLLISION_DEATH))
    elif snake_head.colliderect(right_border):
        pygame.event.post(pygame.event.Event(COLLISION_DEATH))
    elif snake_head.colliderect(upper_border):
        pygame.event.post(pygame.event.Event(COLLISION_DEATH))
    elif snake_head.colliderect(lower_border):
        pygame.event.post(pygame.event.Event(COLLISION_DEATH))

def handle_head_body_collision(snake_head,body_array):

    for z in range(1,len(body_array)):
        if snake_head.colliderect(body_array[z]):
            pygame.event.post(pygame.event.Event(COLLISION_DEATH))

def handle_apple_collision(snake_head,apple):

    if snake_head.colliderect(apple):
        pygame.event.post(pygame.event.Event(COLLISION_EAT))

def death_case(text):

    global score
    draw_text = GAME_OVER_FONT.render(text, 1, BLACK)
    WINDOW.blit(draw_text, ((WIDTH - draw_text.get_width()) // 2, (HEIGHT - draw_text.get_height()) // 2))
    pygame.display.update()
    pygame.time.delay(3000)
    score = 0
    main()

def update_window(snake_head,left_border,right_border,upper_border,lower_border,apple,body_array):

    #WINDOW BACKGROUND
    WINDOW.fill((WHITE))

    #SNAKE STARTING OBJECTSw
    pygame.draw.rect(WINDOW,GREEN,snake_head)

    #SNAKE_CREATED_DURING_PLAY_OBJECTS
    for element in body_array:
        pygame.draw.rect(WINDOW,GREEN,element)

    #BORDERS
    pygame.draw.rect(WINDOW, BLACK, left_border)
    pygame.draw.rect(WINDOW, BLACK, right_border)
    pygame.draw.rect(WINDOW, BLACK, upper_border)
    pygame.draw.rect(WINDOW, BLACK, lower_border)

    #SCORE
    text = "SCORE: "+ str(score)
    draw_text = GAME_OVER_FONT.render(text, 1, BLACK)
    WINDOW.blit(draw_text,(650,25))

    #APPLE
    pygame.draw.rect(WINDOW,RED,apple)

    #update
    pygame.display.update()

def main():

    global score

    counter = 0

    run = True

    clock = pygame.time.Clock()

    snake_head = pygame.Rect(50, 410, SNAKE_WIDTH, SNAKE_HEIGHT)

    snake_head_array = []

    body_array = []

    snake_head_array.append([snake_head.x, snake_head.y])

    left_border = pygame.Rect(0, 0, BORDER_WIDTH, BORDER_HEIGHT)
    right_border = pygame.Rect(WIDTH-BORDER_WIDTH, 0, BORDER_WIDTH, BORDER_HEIGHT)
    upper_border = pygame.Rect(0, 0, BORDER_HEIGHT, BORDER_WIDTH)
    lower_border = pygame.Rect(0, WIDTH-BORDER_WIDTH, BORDER_HEIGHT, BORDER_WIDTH)

    apple = pygame.Rect((WIDTH-APPLE_WIDTH)//2,200,APPLE_WIDTH,APPLE_HEIGHT)

    previous_direction = ''
    current_direction = 'right'

    while run:

        clock.tick(FPS)

        handle_head_body_collision(snake_head,body_array)
        handle_border_collision(snake_head,left_border,right_border,upper_border,lower_border)
        handle_apple_collision(snake_head,apple)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == COLLISION_DEATH:
                death_case("GAME OVER!!!")

            if event.type == COLLISION_EAT:

                score = score + 1

                apple.x = random.randint(70,790)
                apple.y = random.randint(70,790)

                new_part = pygame.Rect(snake_head.x, snake_head.y, SNAKE_WIDTH, SNAKE_HEIGHT)

                body_array.append(new_part)

            #INPUT BUTTON PRESSES

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    previous_direction = current_direction
                    current_direction = 'down'

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    previous_direction = current_direction
                    current_direction = 'up'

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    previous_direction = current_direction
                    current_direction = 'right'

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    previous_direction = current_direction
                    current_direction = 'left'

        #NEW MOVEMENT CODE:

        if current_direction == 'right' and previous_direction != 'left':
            snake_head.x += SNAKE_VELOCITY
            snake_head_array.append([snake_head.x, snake_head.y])
        elif current_direction == 'right' and previous_direction == 'left':
            snake_head.x -= SNAKE_VELOCITY
            snake_head_array.append([snake_head.x, snake_head.y])

        elif current_direction == 'left' and previous_direction != 'right':
            snake_head.x -= SNAKE_VELOCITY
            snake_head_array.append([snake_head.x, snake_head.y])
        elif current_direction == 'left' and previous_direction == 'right':
            snake_head.x += SNAKE_VELOCITY
            snake_head_array.append([snake_head.x, snake_head.y])


        elif current_direction == 'up' and previous_direction != 'down' :
            snake_head.y -= SNAKE_VELOCITY
            snake_head_array.append([snake_head.x, snake_head.y])
        elif current_direction == 'up' and previous_direction == 'down':
            snake_head.y += SNAKE_VELOCITY
            snake_head_array.append([snake_head.x, snake_head.y])


        elif current_direction == 'down' and previous_direction != 'up':
            snake_head.y += SNAKE_VELOCITY
            snake_head_array.append([snake_head.x, snake_head.y])
        elif current_direction == 'down' and previous_direction == 'up':
            snake_head.y -= SNAKE_VELOCITY
            snake_head_array.append([snake_head.x, snake_head.y])

        counter += 1

        for j in range(1,len(body_array)+1):

            position_needed = counter - j

            body_array[j-1].x = snake_head_array[position_needed][0]
            body_array[j-1].y = snake_head_array[position_needed][1]

        update_window(snake_head,left_border,right_border,upper_border,lower_border,apple,body_array)

    exit()
    pygame.exit()

main()