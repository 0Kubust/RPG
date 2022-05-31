import pygame
pygame.init()
#window game
stat_panel = 150
screen_width = 800
screen_height = 400 + stat_panel

screen = pygame.display.set_mode((screen_width, screen_height))
#def col
red = (255, 0 , 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)

#def font
fontA30 = pygame.font.SysFont('Ariel', 30)
fontIntroAl26 = pygame.font.SysFont('Algerian', 26)
fontA26 = pygame.font.SysFont('Ariel', 26)
fontTNR10 = pygame.font.SysFont('Times New Roman', 10)

class Text():
    def __init__(self, text, font, text_col, x, y):
        self.text = text
        self.font = font
        self.text_col = text_col
        self.x = x
        self.y = y

#before first action
start = 'start'
exit_fun = 'exit'
start_display = Text(start, fontIntroAl26, white, 350 + 20, 300)
def draw():
    img = start_display.font.render(start_display.text,True,start_display.text_col)
    screen.blit(img,(start_display.x,start_display.y))