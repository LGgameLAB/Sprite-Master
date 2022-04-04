import pygame
from settings import *

class Dot(pygame.sprite.Sprite):
    def __init__(self, master, **kwargs):
        self.editor = master.editor
        self.master = master
        self.groups = master.components, master.layers.layer1
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos= (winWidth/3, winHeight/3)
        for k, v in kwargs.items():
            self.__dict__[k] = v
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 50, 50)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.circle(self.image, orangeRed, (self.rect.w/2, self.rect.h/2), 25)

class Camera(pygame.sprite.Sprite):

    def __init__(self, master, width=winWidth, height=winHeight):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.game = game
        sprite.Sprite.__init__(self, game.sprites)

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def applyRect(self, rect):
        return rect.move(self.camera.topleft)
        
    def update(self):
        self.target = self.game.currentBlock
        x = 0#x = -self.target.rect.centerx + int(winWidth / 2)
        y = -self.target.rect.centery + int(winHeight / 2)

        self.camera = pygame.Rect(x, y, self.width, self.height)

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
    def __init__(self, master, pos, **kwargs):
        self.master = master
        
        self.onClick = False
        self.groups = master.layers, master.components
        self.wh = (200, 60)
        #          Normal           Selected
        self.colors = (red, white)
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
        mouseRect.move_ip(-self.master.rect.x, -self.master.rect.y)
        if mouseRect.colliderect(self.rect):
            self.hover = True
        
        if self.hover:
            for event in self.master.editor.events:
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

class Part(pygame.sprite.Sprite):
    def __init__(self, master, image, **kwargs):
        self.editor = master.editor
        self.master = master
        self.groups = master.components, master.layers.layer1
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = (0, 0)
        for k, v in kwargs.items():
            self.__dict__[k] = v
        
        self.loadImg(image)
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.rect.topleft = self.pos
    
    def render(self):
        pass

    def update(self):
        print(self.pos)
    
    def loadImg(self, img):
        img = pygame.image.load(img)
        mask = pygame.mask.from_surface(img)
        self.image = pygame.Surface(mask.get_size())
        self.image.blit(img, (0, 0), mask.get_rect())