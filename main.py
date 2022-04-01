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
        self.zoomCenter = pygame.Vector2(0, 0)  
        self.bgColor = yellow
        self.rect = pygame.Rect(0, 0, 300, 300)
        self.image = pygame.Surface(self.rect.size)
    
    def render(self):
        self.image.fill(self.bgColor)
        
        for l in self.layers:
            for i in l:        
                self.image.blit(pygame.transform.scale(i.image, (i.image.get_width()*self.zoom, i.image.get_height()*self.zoom)), i.rect)
    
    def update(self):
        self.components.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEWHEEL:
                print(event)
        self.render()

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
        Dot(self)

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

