import pygame
import texts
pygame.init()

#window game
stat_panel = 150
screen_width = 800
screen_height = 400 + stat_panel
clicked = False
screen = pygame.display.set_mode((screen_width, screen_height))
panel2_frame = pygame.image.load('images/usable/stat2.png').convert_alpha()
inscription_changer = False
#def col
red = (255, 0 , 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)

def draw():
    
    pos = pygame.mouse.get_pos()
    screen.blit(panel2_frame,(0, 0))
    kw = pygame.Rect(350,300,120,30)
    pygame.draw.rect(screen, red, (350, 300, 120, 30))
    texts.draw()
    if kw.collidepoint(pos):
        clicked = False
        if clicked == True:
            inscription_changer = False
            return inscription_changer 
            

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                    pygame.quit()
        else:
            clicked = False
    pygame.display.update()
pygame.quit