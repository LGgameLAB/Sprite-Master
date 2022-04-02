import pygame
from settings import *
from components import Dot

class Layers:
    def __init__(self, *args):
        self.layerCnt = 0
        for l in args:
            if isinstance(l, list):
                self.__dict__["layer"+str(self.layerCnt)] = pygame.sprite.Group(l)
                self.layerCnt += 1
            else:
                raise Exception("Plz pass lists into Layers class")
    
    def __iter__(self):
        # print(self.__dict__)
        return iter([self.__dict__[x] for x in self.__dict__ if x[0:5] == "layer" and isinstance(self.__dict__[x], pygame.sprite.Group)])
    
    def add(self, group=[]):
        self.__dict__["layer"+str(self.layerCnt)] = pygame.sprite.Group(group)
        self.layerCnt += 1
 
class Canvas(pygame.sprite.Sprite):
    def __init__(self, editor):
        self.editor = editor
        self.groups = editor.layers.layer0, editor.components
        super().__init__(self.groups)
        self.layers = Layers( [], [], [], [], [], )
        self.components = pygame.sprite.Group()
        self.zoom = 1
        self.zoomCenter = pygame.Vector2(winWidth/3, winHeight/3)  
        self.bgColor = yellow
        self.rect = pygame.Rect(0, 0, 300, 300)
        self.image = pygame.Surface(self.rect.size)
    
    def render(self):
        self.image.fill(self.bgColor)
        
        for l in self.layers:
            for i in l:  
                scaleRect = self.scale(i.rect)
                if scaleRect.colliderect(self.rect):
                    self.image.blit(pygame.transform.scale(i.image, (int(i.image.get_width()*self.zoom), int(i.image.get_height()*self.zoom))), scaleRect)
    
    def update(self):
        self.components.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEWHEEL:
                print(event)
            if event.type == pygame.MOUSEMOTION:
                self.zoomCenter = pygame.Vector2(pygame.mouse.get_pos())*self.zoom

    
        if checkKey("zoomIn"):
            self.zoom +=0.01*deltaConst
            
            
        if checkKey("zoomOut"):
            self.zoom *=0.995*deltaConst
                    
        self.render()

    def scale(self, rect):
        new = pygame.Rect(0, 0, rect.w*self.zoom, rect.h*self.zoom)
        newPos = (1-self.zoom)*pygame.Vector2(self.zoomCenter) + pygame.Vector2(rect.topleft)*self.zoom 
        new.topleft = newPos
        return new

class Editor:
    def __init__(self):
        self.win = pygame.display.set_mode((winWidth, winHeight))
        self.clock = pygame.time.Clock()
        self.components = pygame.sprite.Group()
        self.layers = Layers( [], [], [], [], [], ) # initializes empty layers in layers container
        self.active = False
        self.new()

    def new(self):
        self.canvas = Canvas(self)
        Dot(self.canvas)
        Dot(self.canvas, pos=[30, 30])

    def run(self):
        self.active = True
        while self.active:
            self.events()
            self.update()
            self.render()

    def events(self):
        self.clock.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            

    def update(self):
        self.components.update()
    
    def render(self):
        self.win.fill(white)
        
        for l in self.layers:
            for i in l:              
                self.win.blit(i.image, i.rect)
        
        pygame.display.update()

    def quit(self):
        self.active = False
        pygame.quit()

if __name__ == '__main__':
    editor = Editor()
    editor.run()

