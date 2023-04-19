import copy
import random
import pygame

pygame.init()


Shop_coin = 0
coin_amount = 0

width = 1920
height = 1080
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('GAME')
font = pygame.font.Font('freesansbold.ttf', 70)
character_selected = 'character.jpg'

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


class Button(pygame.sprite.Sprite):
    def __init__(self, text, x, y, button_size):
        super().__init__()
        self.text = text
        self.x = x
        self.y = y
        self.button_size = button_size
        if self.button_size == 1:
            self.button_size = (200, 100)
        self.draw()

    def draw(self):

        button_text = font.render(self.text, True, 'Black')
        buttonrect = pygame.rect.Rect((self.x, self.y), self.button_size)
        pygame.draw.rect(screen, 'gray', buttonrect, 0, 5)
        pygame.draw.rect(screen, 'black', buttonrect, 2, 5)
        screen.blit(button_text, (self.x + 10, self.y + 10))

    def click(self):
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        buttonrect = pygame.rect.Rect((self.x, self.y), (200, 100))
        if click and buttonrect.collidepoint(mouse_pos):
            return True

        else:
            return False

        player = Player('character.jpg', 0, 100)
def Victory_menu():
    global coin_amount
    coin_text = font.render(str(coin_amount), True, 'black')
    while True:

        celebration = pygame.transform.scale(pygame.image.load('celebration.png'), (1920, 1080))
        screen.blit(celebration, (0,0))
        victory_text = font.render('congratiolations!  +', True, 'black')
        screen.blit(victory_text, (300, 225))

        screen.blit(coin_text, (1000, 225))
        screen.blit(pygame.transform.scale(pygame.image.load('coin.png'), (75, 75)), (1050, 225))
        coin_amount = 0
        new_game_button = Button('New Game?', 400, 300, (500,100))
        shop_button = Button('shop', 400, 400, (500, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if new_game_button.click():
                Game()
            if shop_button.click():
                Shop()
            pygame.display.flip()
def death_screen():
    while True:
        
        game_over_img = pygame.transform.scale(pygame.image.load('new_game_over.jpg'), (1920, 1080))
        screen.blit(game_over_img, (0, 0))
        new_game_button = Button('New Game?', 700, 800, (500,100))
        shop_button = Button('shop', 700, 900, (500, 100))
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
            if new_game_button.click():
                Game()
            if shop_button.click():
                Shop()
        pygame.display.flip()
def Game():
    while True:
        global coin_amount
        global Shop_coin
        beakers_boxes = []
        player = Player(character_selected, 0, 100)
        fps = 60
        timer = pygame.time.Clock()
        speed = 2.5


        color_choices = ['red', 'orange', 'light blue', 'dark blue', 'dark green', 'pink', 'purple', 'dark gray',
                          'light green', 'yellow', 'white', 'red', 'orange', 'light blue', 'dark blue', 'dark green', 'pink', 'purple', 'dark gray',
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

        coin_group = pygame.sprite.Group()
        amount_of_coins_on_screen = 10
        def coins():
            coin_group.empty()
            for i in range(amount_of_coins_on_screen):

                new_coin = Coin(random.randint(100, 1800), random.randint(100, 600))
                coin_group.add(new_coin)

        coins()


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
            coin_group.draw(screen)
            coin_group.update()

            screen.blit(pygame.transform.scale(pygame.image.load('coin.png'), (75, 75)), ( 1850, 980))
            coin_text = font.render(str(coin_amount), True, 'black')
            screen.blit(coin_text, (1800, 980))
        
        def hit():
            global beaker_colors
            global coin_amount
            for i in beakers_boxes:
                if pygame.Rect.colliderect(player.hitbox, i):
                    death_screen()
                for j in coin_group:
                    if pygame.Rect.colliderect(i, j):
                        coin_group.remove(j)
                        new_coin = Coin(random.randint(100, 1800), random.randint(100, 600))
                        coin_group.add(new_coin)

            for i in coin_group:
                if pygame.Rect.colliderect(player.hitbox, i.hitbox):
                    coin_group.remove(i)
                    coin_amount += 1

        # main game loop


        while True:
            screen.fill('black')

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
                    pygame.quit()


                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        coin_amount = 0
                        Main_menu()
                    if event.key == pygame.K_SPACE:
                        pygame.time.set_timer(pygame.USEREVENT, 100)
                        yaxis = False
                    if event.key == pygame.K_y:
                        win = True
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
                Shop_coin += coin_amount

                Victory_menu()



            # display all drawn items on screen, exit pygame if run == False
            pygame.display.flip()
def Main_menu():
        while True:
            screen.blit(pygame.image.load('background.png'), (0, 0))
            #buttons
            start_button = Button('Start', 100, 100, 1)
            shop_button = Button('shop', 100, 200, 1)
            quit_button = Button('quit', 100, 300, 1)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                #buttons
                if start_button.click():
                    Game()
                if shop_button.click():
                    Shop()
                if quit_button.click():
                    pygame.quit()
            pygame.display.flip()
character2_bought = False
character3_bought = False
character4_bought = False

def Shop():
    while True:

        while True:
            print(pygame.mouse.get_pos)
            global character_selected
            global Shop_coin

            char1pic = pygame.transform.scale(pygame.image.load('character.jpg'), (300, 300))
            char2pic = pygame.transform.scale(pygame.image.load('character2.jpg'), (300, 300))
            char3pic = pygame.transform.scale(pygame.image.load('character3.jpg'), (300, 300))
            char4pic = pygame.transform.scale(pygame.image.load('character4.jpg'), (300, 300))
            global character2_bought
            global character3_bought
            global character4_bought
            screen.blit(pygame.image.load('background.png'), (0,0))

            screen.blit(pygame.transform.scale(pygame.image.load('coin.png'), (75, 75)), (1850, 980))


            coin_text = font.render(str(Shop_coin), True, 'black')
            screen.blit(coin_text, (1800, 980))
            #
            character1_button = Button('select', 100, 600, 1)

            if character2_bought == False:
                character2_button = Button('5', 800, 600, 1)
                screen.blit(pygame.transform.scale(pygame.image.load('coin.png'), (75, 75)), (860, 610))
            elif character2_bought == True:
                character2_button = Button('select', 800, 600, 1)
            if character3_bought == False:
                character3_button = Button('10', 1500, 600, 1)
                screen.blit(pygame.transform.scale(pygame.image.load('coin.png'), (75, 75)), (1600, 610))
            elif character3_bought == True:
                character3_button = Button('select', 1500, 600, 1)

            if character4_bought == False:
                character4_button = Button('15', 1000, 160, 1)
                screen.blit(pygame.transform.scale(pygame.image.load('coin.png'), (75, 75)), (1100, 170))
            elif character4_bought == True:
                character4_button = Button('select', 1000, 160, 1)

            screen.blit(char1pic, (100, 300))
            screen.blit(char2pic, (800, 300))
            screen.blit(char3pic, (1500, 300))
            screen.blit(char4pic, (700, 75))
        #selecting'
        
            if character1_button.click():
                character_selected = 'character.jpg'

            if character2_button.click() and character2_bought:
                character_selected = 'character2.jpg'
            elif character2_button.click() and character2_bought == False:
                if Shop_coin >= 5:
                    character2_bought = True
                    Shop_coin -= 5
                    character_selected = 'character2.jpg'
            if character3_button.click() and character3_bought:
                character_selected = 'character3.jpg'
            elif character3_button.click() and character3_bought == False:
                if Shop_coin >= 10:
                    character3_bought = True
                    Shop_coin -= 10
                    character_selected = 'character3.jpg'
            if character4_button.click() and character4_bought:
                character_selected = 'character4.jpg'
            elif character4_button.click() and character4_bought == False:
                if Shop_coin >= 15:
                    character4_bought = True
                    Shop_coin -= 15
                    character_selected = 'character4.jpg'

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Main_menu()
                    if event.key == pygame.K_p:
                        Shop_coin += 1

                pygame.display.flip()
Main_menu()
pygame.quit()