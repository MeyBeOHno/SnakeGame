import pygame
import time
import random

pygame.init()

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
dark_green = (0, 100, 0)
brown = (139, 69, 19)
light_brown = (222, 184, 135)
gray = (169, 169, 169)
yellow = (255, 255, 102)

# Define screen dimensions
dis_width = 800
dis_height = 600

# Create the screen
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Змейка')

# Define game speed
clock = pygame.time.Clock()

snake_block = 20
snake_speed_easy = 10
snake_speed_medium = 20
snake_speed_hard = 30

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Load and scale images
def load_and_scale_image(image_path, size):
    image = pygame.image.load(image_path)
    return pygame.transform.scale(image, (size, size))

cherry_image = load_and_scale_image('cherry.png', int(snake_block))
raspberry_image = load_and_scale_image('raspberry.png', int(snake_block))

def message(msg, color, y_displace=0):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3 + y_displace])

def draw_obstacles(obstacles):
    for obs in obstacles:
        pygame.draw.rect(dis, red, [obs[0], obs[1], snake_block, snake_block])

def draw_button(text, color, x, y, width, height, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(dis, color, [x, y, width, height])
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(dis, color, [x, y, width, height])

    small_text = pygame.font.SysFont("bahnschrift", 20)
    text_surf = small_text.render(text, True, white)
    text_rect = text_surf.get_rect(center=(x + width / 2, y + height / 2))
    dis.blit(text_surf, text_rect)

def set_level_easy():
    global snake_speed, obstacles
    snake_speed = snake_speed_easy
    obstacles = []
    gameLoop()

def set_level_medium():
    global snake_speed, obstacles
    snake_speed = snake_speed_medium
    obstacles = []
    gameLoop()

def set_level_hard():
    global snake_speed, obstacles
    snake_speed = snake_speed_hard
    obstacles = [[x, 0] for x in range(0, dis_width, snake_block)] + [
        [x, dis_height - snake_block] for x in range(0, dis_width, snake_block)] + [
        [0, y] for y in range(0, dis_height, snake_block)] + [
        [dis_width - snake_block, y] for y in range(0, dis_height, snake_block)]
    gameLoop()

def two_player_game():
    global snake_speed, obstacles
    snake_speed = snake_speed_medium
    obstacles = []
    two_player_game_loop()

def game_intro():
    intro = True
    while intro:
        dis.fill(blue)
        message("Выберите уровень сложности", white, -100)
        draw_button("Легкий", green, dis_width / 2 - 50, dis_height / 2 - 90, 100, 50, set_level_easy)
        draw_button("Средний", yellow, dis_width / 2 - 50, dis_height / 2 - 30, 100, 50, set_level_medium)
        draw_button("Сложный", red, dis_width / 2 - 50, dis_height / 2 + 30, 100, 50, set_level_hard)
        draw_button("Два игрока", blue, dis_width / 2 - 50, dis_height / 2 + 90, 100, 50, two_player_game)
        draw_button("Выход", gray, dis_width - 110, 10, 100, 50, pygame.quit)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

def age_input_screen():
    age_input = ""
    input_active = True
    while input_active:
        dis.fill(blue)
        message("Введите свой возраст (очки для победы):", white, -50)
        age_text = font_style.render(age_input, True, white)
        dis.blit(age_text, [dis_width / 3, dis_height / 2])
        draw_button("ОК", green, dis_width / 2 - 50, dis_height / 2 + 50, 100, 50, None)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if age_input.isdigit():
                        global points_to_win
                        points_to_win = int(age_input)
                        input_active = False
                        game_intro()
                elif event.key == pygame.K_BACKSPACE:
                    age_input = age_input[:-1]
                else:
                    age_input += event.unicode

def message_multi_line(text, color):
    lines = text.split("\n")
    for i, line in enumerate(lines):
        message(line, color, i * 40)

def check_food_collision(x, y, food_position):
    return x == food_position[0] and y == food_position[1]

def gameLoop():
    game_over = False
    game_close = False

    x1, y1 = dis_width / 2, dis_height / 2
    x1_change, y1_change = 0, 0

    last_direction = ""

    snake_List = []
    Length_of_snake = 1

    cherry_position = food_spawning()

    start_time = time.time()

    while not game_over:

        while game_close:
            dis.fill(blue)
            message_multi_line("Проигрыш!\nНажмите Q для выхода или C для новой игры", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_intro()
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and last_direction != 'RIGHT':
                    x1_change = -snake_block
                    y1_change = 0
                    last_direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and last_direction != 'LEFT':
                    x1_change = snake_block
                    y1_change = 0
                    last_direction = 'RIGHT'
                elif event.key == pygame.K_UP and last_direction != 'DOWN':
                    y1_change = -snake_block
                    x1_change = 0
                    last_direction = 'UP'
                elif event.key == pygame.K_DOWN and last_direction != 'UP':
                    y1_change = snake_block
                    x1_change = 0
                    last_direction = 'DOWN'

        x1 = (x1 + x1_change) % dis_width
        y1 = (y1 + y1_change) % dis_height

        dis.fill(blue)

        draw_obstacles(obstacles)

        # Draw cherry
        dis.blit(cherry_image, cherry_position)

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for segment in snake_List[:-1]:
            if segment == snake_Head:
                game_close = True

        for segment in snake_List:
            pygame.draw.circle(dis, dark_green, (segment[0] + snake_block // 2, segment[1] + snake_block // 2), snake_block // 2)

        pygame.draw.circle(dis, red, (snake_List[-1][0] + snake_block // 2, snake_List[-1][1] + snake_block // 2), snake_block // 2)

        # Check for snake 1 eating food
        if check_food_collision(x1, y1, cherry_position):
            cherry_position = food_spawning()
            Length_of_snake += 1

        for obs in obstacles:
            if x1 == obs[0] and y1 == obs[1]:
                game_close = True

        display_score(Length_of_snake - 1, start_time)

        if Length_of_snake - 1 >= points_to_win:
            dis.fill(blue)
            message("Игрок 1 Победил!", yellow, -50)
            message(f"Количество очков: {Length_of_snake - 1}", white, 50)
            pygame.display.update()
            time.sleep(2)
            game_intro()

        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()
    quit()
def food_spawning():
    foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
    return foodx, foody

def display_score(score, start_time, player=1):
    elapsed_time = time.time() - start_time
    value = score_font.render(f"Игрок {player} Очки: {score} Время: {int(elapsed_time)}с", True, white)
    if player == 1:
        dis.blit(value, [0, 0])
    else:
        dis.blit(value, [0, 40])

# Function for two player game mode
def two_player_game_loop():
    global game_over, game_close
    game_over = False
    game_close = False

    x1, y1 = dis_width / 2, dis_height / 2
    x1_change, y1_change = 0, 0

    x2, y2 = dis_width / 4, dis_height / 4
    x2_change, y2_change = 0, 0

    last_direction1 = ""
    last_direction2 = ""

    snake1_List = []
    Length_of_snake1 = 1

    snake2_List = []
    Length_of_snake2 = 1

    cherry_position = food_spawning()
    raspberry_position = food_spawning()

    start_time = time.time()

    while not game_over:

        while game_close:
            dis.fill(blue)
            message_multi_line("Проигрыш!\nНажмите Q для выхода или C для новой игры", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_intro()
                    if event.key == pygame.K_c:
                        two_player_game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and last_direction1 != 'RIGHT':
                    x1_change = -snake_block
                    y1_change = 0
                    last_direction1 = 'LEFT'
                elif event.key == pygame.K_RIGHT and last_direction1 != 'LEFT':
                    x1_change = snake_block
                    y1_change = 0
                    last_direction1 = 'RIGHT'
                elif event.key == pygame.K_UP and last_direction1 != 'DOWN':
                    y1_change = -snake_block
                    x1_change = 0
                    last_direction1 = 'UP'
                elif event.key == pygame.K_DOWN and last_direction1 != 'UP':
                    y1_change = snake_block
                    x1_change = 0
                    last_direction1 = 'DOWN'
                elif event.key == pygame.K_a and last_direction2 != 'RIGHT':
                    x2_change = -snake_block
                    y2_change = 0
                    last_direction2 = 'LEFT'
                elif event.key == pygame.K_d and last_direction2 != 'LEFT':
                    x2_change = snake_block
                    y2_change = 0
                    last_direction2 = 'RIGHT'
                elif event.key == pygame.K_w and last_direction2 != 'DOWN':
                    y2_change = -snake_block
                    x2_change = 0
                    last_direction2 = 'UP'
                elif event.key == pygame.K_s and last_direction2 != 'UP':
                    y2_change = snake_block
                    x2_change = 0
                    last_direction2 = 'DOWN'

        x1 = (x1 + x1_change) % dis_width
        y1 = (y1 + y1_change) % dis_height

        x2 = (x2 + x2_change) % dis_width
        y2 = (y2 + y2_change) % dis_height

        dis.fill(blue)

        draw_obstacles(obstacles)

        # Draw berries
        dis.blit(cherry_image, cherry_position)
        dis.blit(raspberry_image, raspberry_position)

        # Snake 1
        snake1_Head = [x1, y1]
        snake1_List.append(snake1_Head)
        if len(snake1_List) > Length_of_snake1:
            del snake1_List[0]

        # Snake 2
        snake2_Head = [x2, y2]
        snake2_List.append(snake2_Head)
        if len(snake2_List) > Length_of_snake2:
            del snake2_List[0]

        # Draw snake 1
        for segment in snake1_List[:-1]:
            if segment == snake1_Head:
                game_close = True
        for segment in snake1_List:
            pygame.draw.circle(dis, dark_green, (segment[0] + snake_block // 2, segment[1] + snake_block // 2),
                               snake_block // 2)
        pygame.draw.circle(dis, red, (snake1_List[-1][0] + snake_block // 2, snake1_List[-1][1] + snake_block // 2),
                           snake_block // 2)

        # Draw snake 2
        for segment in snake2_List[:-1]:
            if segment == snake2_Head:
                game_close = True
        for segment in snake2_List:
            pygame.draw.circle(dis, green, (segment[0] + snake_block // 2, segment[1] + snake_block // 2),
                               snake_block // 2)
        pygame.draw.circle(dis, black, (snake2_List[-1][0] + snake_block // 2, snake2_List[-1][1] + snake_block // 2),
                           snake_block // 2)

        # Check for snake 1 eating food
        if check_food_collision(x1, y1, cherry_position):
            cherry_position = food_spawning()
            Length_of_snake1 += 1

        # Check for snake 2 eating raspberry
        if check_food_collision(x2, y2, raspberry_position):
            raspberry_position = food_spawning()
            Length_of_snake2 += 1

        # Check for collision with obstacles
        for obs in obstacles:
            if x1 == obs[0] and y1 == obs[1] or x2 == obs[0] and y2 == obs[1]:
                game_close = True

        # Display scores
        display_score(Length_of_snake1 - 1, start_time, player=1)
        display_score(Length_of_snake2 - 1, start_time, player=2)

        # Check for winning condition
        if Length_of_snake1 - 1 >= points_to_win:
            dis.fill(blue)
            message("Игрок 1 Победил!", yellow, -50)
            message(f"Количество очков: {Length_of_snake1 - 1}", white, 50)
            pygame.display.update()
            time.sleep(2)
            game_intro()

        if Length_of_snake2 - 1 >= points_to_win:
            dis.fill(blue)
            message("Игрок 2 Победил!", yellow, -50)
            message(f"Количество очков: {Length_of_snake2 - 1}", white, 50)
            pygame.display.update()
            time.sleep(2)
            game_intro()

        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()
    quit()


# Start the game
age_input_screen()


