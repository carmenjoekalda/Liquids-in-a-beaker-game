import pygame
pygame.init()

# window size
width = 1600
height = 900
screen = pygame.display.set_mode((width, height))

# button sizes
button_width = 200
button_height = 100

# button colors and fonts
button_color = (255, 255, 255)
button_hover_color = (200, 200, 200)
button_font = pygame.font.Font(None, 30)

# list of button positions and labels
buttons = [
    ((width/2 - button_width/2, height/2 - button_height/2 - 50), "Start"),
    ((width/2 - button_width/2, height/2 - button_height/2 + 50), "Customize"),
    ((width/2 - button_width/2, height/2 - button_height/2 + 150), "Quit")
]

# function to draw a button and return its rectangle
def draw_button(text, pos, color):
    button_rect = pygame.Rect(pos[0], pos[1], button_width, button_height)
    pygame.draw.rect(screen, color, button_rect)
    text_surf = button_font.render(text, True, (0, 0, 0))
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)
    return button_rect

# draw the buttons and return their rectangles
button_rects = [draw_button(label, pos, button_color) for pos, label in buttons]

# load the background image and blit it onto the screen
background_image = pygame.image.load('background.png').convert()
screen.blit(background_image, (0, 0))

# boolean to check if start button was clicked or the customize button was clicked
start_button_clicked = False
customize_button_clicked = False


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, rect in enumerate(button_rects):
                if rect.collidepoint(event.pos):
                    if i == 0:
                        # start button clicked
                        start_button_clicked = True
                    elif i == 1:
                        # customize button clicked
                        customize_button_clicked = True
                    elif i == 2:
                        # quit button clicked
                        pygame.quit()
                        quit()

   # clear the screen and draw the buttons
    screen.blit(background_image, (0, 0))
    for i, (pos, label) in enumerate(buttons):
        if button_rects:
            rect = button_rects[i]
            if rect.collidepoint(pygame.mouse.get_pos()):
                if i == 1: # hover on customize button
                    draw_button(label, pos, button_hover_color)
                else:
                    draw_button(label, pos, button_color)
            else:
                draw_button(label, pos, button_color)

    # if start button was clicked, show "Top tier gameplay" text and hide the buttons
    if start_button_clicked:
        screen.fill((0, 0, 0))
        text_surf = button_font.render("Top tier gameplay", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(width/2, height/2))
        screen.blit(text_surf, text_rect)
        button_rects = []  # clear the button rectangles
    
    # if customize button was clicked, show "This is where you would customize" text and hide the buttons
    if customize_button_clicked:
        screen.fill((0, 0, 0))
        text_surf = button_font.render("This is where you would customize", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(width/2, height/2))
        screen.blit(text_surf, text_rect)
        button_rects = []  # clear the button rectangles

    # if customize button was clicked, show "This is where you would customize" text and hide the buttons
    if customize_button_clicked:
        screen.fill((0, 0, 0))
        text_surf = button_font.render("This is where you would customize", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(width/2, height/2))
        screen.blit(text_surf, text_rect)
        button_rects = []  # clear the button rectangles
    
    pygame.display.update()