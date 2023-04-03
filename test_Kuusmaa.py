import pygame

pygame.init()
win = pygame.display.set_mode((1600, 900))
win.fill("white")


#background
background_img = pygame.image.load("Background.jpg")
background = pygame.transform.scale(background_img, (1600, 900))
clock = pygame.time.Clock()
#player 
img = pygame.image.load("charcter.jpg")
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        image = pygame.image.load("charcter.jpg")
        self.image = pygame.transform.scale(image, (100, 50))
            
#pipes



player = Player(100, 500)
player.x = 100
player.y = 400

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.y -= 100

    win.blit(background, (0, 0))

    win.blit(player.image, (player.x, player.y))
    #pipes
    #pipe 1

    pygame.draw.rect(win,("green"), pygame.Rect(400,500, 100, 400))
    pygame.draw.rect(win,("green"), pygame.Rect(400,0, 100, 200))

    

    print(pygame.mouse.get_pos())
    #death
    if player.x > 3900 and player.x < 490 and player.y > 490 :
        player.x = 100
        player.y = 400

    player.x += 3
    if player.x > 1600:
        player.x = 0
    player.y += 2

    


    pygame.display.update()
    