import copy
import random
import pygame


# initialize pygame
pygame.init()
beakers_boxes = []
# create game variables
width = 1920
height = 1080
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('BEAKER GAME')
font = pygame.font.Font('freesansbold.ttf', 70)
fps = 60
timer = pygame.time.Clock()
speed = 2.5
coin_amount = 0

color_choices = ['red', 'orange', 'light blue', 'dark blue', 'dark green', 'pink', 'purple', 'dark gray',
                 'brown', 'light green', 'yellow', 'white', 'red', 'orange', 'light blue', 'dark blue', 'dark green', 'pink', 'purple', 'dark gray',
                 'brown', 'light green', 'yellow', 'white']
beaker_colors = []
initial_colors = []
background = pygame.image.load('background.png')
# 10 - 14 beakers, always start with two empty
beakers = 10
new_game = True
selected = False
beaker_rects = []
select_rect = 100
win = False

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('coin.png'), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.x = x
        self.y = y
        self.hitbox = pygame.Rect(x - 25, y - 25, 50, 50)
    def update(self):

        pygame.draw.rect(screen, ('red'), self.hitbox, 2)

coins = pygame.sprite.Group()
coin1 = Coin(700, 100)
coin2 = Coin(300, 100)
coins.add(coin1, coin2)

class Player:
    def __init__(self, picture_path, x, y):
        super().__init__()
        image = pygame.image.load(picture_path)
        self.image = pygame.transform.scale(image, (200, 200))
        self.x = x
        self.y = y
        self.hitbox = pygame.Rect(self.x + 60, self.y + 70, 60, 60)
    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        pygame.draw.rect(screen, ('red'), self.hitbox, 2)
        self.hitbox = pygame.Rect(self.x + 60, self.y + 70, 60, 60)
player = Player('tempflap.png', 0, 100)
yaxis = True
def movement():
    keypress = pygame.key.get_pressed()
    if yaxis == True:
        player.y += speed * 3
    else:
        player.y -= 20
    player.x += speed - 1
    if keypress[pygame.K_a]:
        player.x -= speed
    if keypress[pygame.K_d]:
        player.x += speed
    if player.x > 1920:
        player.x = 0
    if player.y > 1000:
        player.y = 100
# select a number of beakers and pick random colors
def generate_start():
    beakers_number = 12
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

    beakers_per_row = beakers_num // 2
    spacing = width / beakers_per_row

    for i in range(beakers_per_row):
        for j in range(len(beaker_cols[i])):
            pygame.draw.rect(screen, color_choices[beaker_cols[i][j]], [500 + spacing * i, 200 - (50 * j), 65, 50], 0, 3)
        box = pygame.draw.rect(screen, 'blue', [500 + spacing * i, 50, 65, 200], 5, 5)
        if select_rect == i:
            pygame.draw.rect(screen, 'green', [500 + spacing * i, 50, 65, 200], 3, 5)
        beaker_boxes.append(box)
        beakers_boxes.append(box)
    for i in range(beakers_per_row):
        for j in range(len(beaker_cols[i + beakers_per_row])):
            pygame.draw.rect(screen, color_choices[beaker_cols[i + beakers_per_row][j]], [5 + spacing * i,
                                                                                          600 - (50 * j), 65, 50], 0, 3)
        box = pygame.draw.rect(screen, 'blue', [5 + spacing * i, 450, 65, 200], 5, 5)
        if select_rect == i + beakers_per_row:
            pygame.draw.rect(screen, 'green', [5 + spacing * i, 450, 65, 200], 3, 5)
        beaker_boxes.append(box)
        beakers_boxes.append(box)
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


def draw():
    screen.blit(background, ( 0,0))
    coins.draw(screen)
    coins.update()

    screen.blit(pygame.transform.scale(pygame.image.load('coin.png'), (75, 75)), ( 1850, 980))
    coin_text = font.render(str(coin_amount), True, 'black')
    screen.blit(coin_text, (1800, 980))
    print(pygame.mouse.get_pos())
def hit():
    global beaker_colors
    global coin_amount
    for i in beakers_boxes:
        if pygame.Rect.colliderect(player.hitbox, i):
            beaker_colors = copy.deepcopy(initial_colors)
            player.x = 0
            player.y = 100
    for i in coins:
        if pygame.Rect.colliderect(player.hitbox, i.hitbox):
            coins.remove(i)
            coin_amount += 1
            print(coin_amount)


# main game loop
run = True
while run:
    draw()
    hit()
    player.draw()
    movement()
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


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pygame.time.set_timer(pygame.USEREVENT, 100)
                yaxis = False
        if event.type == pygame.USEREVENT:
            yaxis = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_l:
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


    # display all drawn items on screen, exit pygame if run == False
    pygame.display.flip()
pygame.quit()