import pygame

pygame.init()
win = pygame.display.set_mode((900,900))
win.fill((255,255,255))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    pygame.display.update()
