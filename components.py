import pygame
from settings import *

class Dot(pygame.sprite.Sprite):
    def __init__(self, master, **kwargs):
        self.editor = master.editor
        self.master = master
        self.groups = master.components, master.layers.layer1
        pygame.sprite.Sprite.__init__(self, self.groups)
        pos= (winWidth/3, winHeight/3)
        for k, v in kwargs.items():
            self.__dict__[k] = v
        self.rect = pygame.Rect(pos[0], pos[1], 50, 50)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.circle(self.image, orangeRed, (self.rect.w/2, self.rect.h/2), 25)

class Button(pygame.sprite.Sprite):
    '''
    A menu object that that stores a clicked value when hovered over
    Arguments
    |    Button.text [str] - stores optional text value
    |    Button.colors [tup] - Stores colors 
    |    Button.center [bool] - Stores whether text is centered or not
    Values
    |    Button.clicked [bool] - stores whether it has been clicked or ot since initiation
    |    Button.
    '''
    def __init__(self, editor, pos, **kwargs):
        self.editor = editor
        
        self.onClick = False
        self.groups = editor.layers
        self.wh = (200, 60)
        #          Normal           Selected
        self.colors = (colors.yellow, (255, 255, 255))
        self.spriteInit = False
        self.hover = False
        self.clicked = False
        self.instaKill = False
        self.text = ''
        self.center = False
        for k, v in kwargs.items():
            self.__dict__[k] = v

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect = pygame.Rect(0, 0, 20, 20)
        self.rect.size = self.wh
        self.rect.x, self.rect.y = pos
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        self.rendText = fonts["sys"].render(self.text, True, black)
        self.textRect = self.rendText.get_rect()
        if self.center:
            self.textRect.center = pygame.Rect(0, 0, self.rect.width, self.rect.height).center
        else:
            self.textRect.x += 2
            self.textRect.y += 2

    def update(self):
        self.image = pygame.Surface(self.rect.size)
        self.hover = False
        self.clicked = False
        mouseRect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)
        if mouseRect.colliderect(self.rect):
            self.hover = True
        
        if self.hover:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked = True
                    if self.onClick:
                        self.onClick()
                        if self.instaKill:
                            self.kill()

            self.image.fill(self.colors[1])
        else:
            self.image.fill(self.colors[0])
        
        self.image.blit(self.rendText, self.textRect)
    
    def reset(self):
        self.clicked = False