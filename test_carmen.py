# import modules
import copy
import random
import pygame

# initialize pygame
pygame.init()

# create game variables
width = 600
height = 500
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('BEAKER GAME')
font = pygame.font.Font('freesansbold.ttf', 28)
fps = 60
timer = pygame.time.Clock()
color_choices = ['red', 'orange', 'light blue', 'dark blue', 'dark green', 'pink', 'purple', 'dark gray',
                 'brown', 'light green', 'yellow', 'white']
beaker_colors = []
initial_colors = []
# 10 - 14 beakers, always start with two empty
beakers = 10
new_game = True
selected = False
beaker_rects = []
select_rect = 100
win = False



# select a number of beakers and pick random colors
def generate_start():
    beakers_number = random.randint(10, 14)
    beakers_colors = []
    available_colors = []
    for i in range(beakers_number):
        beakers_colors.append([])
        if i < beakers_number - 2:
            for j in range(4):
                available_colors.append(i)
    for i in range(beakers_number - 2):
        for j in range(4):
            color = random.choice(available_colors)
            beakers_colors[i].append(color)
            available_colors.remove(color)
    print(beakers_colors)
    print(beakers_number)
    return beakers_number, beakers_colors


# draw all beakers and colors on screen, indicate which beaker was selected
def draw_beakers(beakers_num, beaker_cols):
    beaker_boxes = []
    if beakers_num % 2 == 0:
        beakers_per_row = beakers_num // 2
        offset = False
    else:
        beakers_per_row = beakers_num // 2 + 1
        offset = True
    spacing = width / beakers_per_row
    for i in range(beakers_per_row):
        for j in range(len(beaker_cols[i])):
            pygame.draw.rect(screen, color_choices[beaker_cols[i][j]], [5 + spacing * i, 200 - (50 * j), 65, 50], 0, 3)
        box = pygame.draw.rect(screen, 'blue', [5 + spacing * i, 50, 65, 200], 5, 5)
        if select_rect == i:
            pygame.draw.rect(screen, 'green', [5 + spacing * i, 50, 65, 200], 3, 5)
        beaker_boxes.append(box)
    if offset:
        for i in range(beakers_per_row - 1):
            for j in range(len(beaker_cols[i + beakers_per_row])):
                pygame.draw.rect(screen, color_choices[beaker_cols[i + beakers_per_row][j]],
                                 [(spacing * 0.5) + 5 + spacing * i, 450 - (50 * j), 65, 50], 0, 3)
            box = pygame.draw.rect(screen, 'blue', [(spacing * 0.5) + 5 + spacing * i, 300, 65, 200], 5, 5)
            if select_rect == i + beakers_per_row:
                pygame.draw.rect(screen, 'green', [(spacing * 0.5) + 5 + spacing * i, 300, 65, 200], 3, 5)
            beaker_boxes.append(box)
    else:
        for i in range(beakers_per_row):
            for j in range(len(beaker_cols[i + beakers_per_row])):
                pygame.draw.rect(screen, color_choices[beaker_cols[i + beakers_per_row][j]], [5 + spacing * i,
                                                                                          450 - (50 * j), 65, 50], 0, 3)
            box = pygame.draw.rect(screen, 'blue', [5 + spacing * i, 300, 65, 200], 5, 5)
            if select_rect == i + beakers_per_row:
                pygame.draw.rect(screen, 'green', [5 + spacing * i, 300, 65, 200], 3, 5)
            beaker_boxes.append(box)
    return beaker_boxes


#  determine the top color of the selected beaker and destination beaker, how long a chain of that color to move
def calc_move(colors, selected_rect, destination):
    chain = True
    color_on_top = 100
    length = 1
    color_to_move = 100
    if len(colors[selected_rect]) > 0:
        color_to_move = colors[selected_rect][-1]
        for i in range(1, len(colors[selected_rect])):
            if chain:
                if colors[selected_rect][-1 - i] == color_to_move:
                    length += 1
                else:
                    chain = False
    if 4 > len(colors[destination]):
        if len(colors[destination]) == 0:
            color_on_top = color_to_move
        else:
            color_on_top = colors[destination][-1]
    if color_on_top == color_to_move:
        for i in range(length):
            if len(colors[destination]) < 4:
                if len(colors[selected_rect]) > 0:
                    colors[destination].append(color_on_top)
                    colors[selected_rect].pop(-1)
    print(colors, length)
    return colors


# check if every beaker is either empty or has 4 of the same color in it
def check_victory(colors):
    won = True
    for i in range(len(colors)):
        if len(colors[i]) > 0:
            if len(colors[i]) != 4:
                won = False
            else:
                main_color = colors[i][-1]
                for j in range(len(colors[i])):
                    if colors[i][j] != main_color:
                        won = False
    return won


# main game loop
run = True
while run:
    screen.fill([0, 0, 0])
    timer.tick(fps)
    # generate game board, make a copy of the colors for restarting
    if new_game:
        beakers, beaker_colors = generate_start()
        initial_colors = copy.deepcopy(beaker_colors)
        new_game = False
    # draw beakers every cycle
    else:
        beaker_rects = draw_beakers(beakers, beaker_colors)
    # check for victory every cycle
    win = check_victory(beaker_colors)
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                beaker_colors = copy.deepcopy(initial_colors)
            elif event.key == pygame.K_RETURN:
                new_game = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not selected:
                for item in range(len(beaker_rects)):
                    if beaker_rects[item].collidepoint(event.pos):
                        selected = True
                        select_rect = item
            else:
                for item in range(len(beaker_rects)):
                    if beaker_rects[item].collidepoint(event.pos):
                        dest_rect = item
                        beaker_colors = calc_move(beaker_colors, select_rect, dest_rect)
                        selected = False
                        select_rect = 100
    # draw victory text when winning, show restart on the top
    if win:
        victory_text = font.render('You Won! Press Enter for a new board!', True, 'white')
        screen.blit(victory_text, (30, 265))
    restart_text = font.render('Stuck? Space-Restart, Enter-New Board!', True, 'white')
    screen.blit(restart_text, (10, 10))

    # display all drawn items on screen, exit pygame if run == False
    pygame.display.flip()
pygame.quit()