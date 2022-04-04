import pygame
from settings import *
from components import Dot, Button
from funcs import importPart

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

class ToolBar(pygame.sprite.Sprite):
    def __init__(self, editor):
        self.editor = editor
        self.groups = editor.layers.layer0, editor.components
        super().__init__(self.groups)
        self.layers = Layers( [], [], [], [], [], )
        # self.camera = Camera()
        self.components = pygame.sprite.Group()
        self.bgColor = black
        self.rect = pygame.Rect(0, winHeight-50, winWidth, 50)
        self.image = pygame.Surface(self.rect.size)
        self.new()
    
    def new(self):
        self.importBtn = Button(self, (0, 0), wh= (100, 50), onClick=lambda: importPart(self), text="Load Part", center=True)
    
    def render(self):
        self.image.fill(self.bgColor)
        
        for l in self.layers:
            for i in l:
                self.image.blit(i.image, i.rect)

    def update(self):
        self.components.update()
        self.render()

class Canvas(pygame.sprite.Sprite):
    def __init__(self, editor):
        self.editor = editor
        self.groups = editor.layers.layer0, editor.components
        super().__init__(self.groups)
        self.layers = Layers( [], [], [], [], [], )
        # self.camera = Camera()
        self.components = pygame.sprite.Group()
        self.zoom = 1  
        self.bgColor = yellow
        self.rect = pygame.Rect(0, 0, 300, 300)
        self.zoomCenter = pygame.Vector2(self.rect.w/2, self.rect.h/2)
        self.image = pygame.Surface(self.rect.size)
    
    def render(self):
        self.image.fill(self.bgColor)
        
        for l in self.layers:
            for i in l:  
                scaleRect = self.scale(i.rect)
                print(scaleRect.topleft)
                if scaleRect.colliderect(self.rect.move(-self.rect.x, -self.rect.y)):
                    self.image.blit(pygame.transform.scale(i.image, (int(i.image.get_width()*self.zoom), int(i.image.get_height()*self.zoom))), scaleRect)
    
    def update(self):
        self.components.update()
        for event in self.editor.events:
            pass
            # if event.type == pygame.MOUSEWHEEL:
                # if event.y > 0:
                    # self.zoom = min(self.zoom+0.08*deltaConst, 3)
                    # self.setZoomCenter() if self.zoom < 5 else None
                # else:
                    # self.zoom = max(self.zoom*0.92*deltaConst, 0.5)
                    # self.setZoomCenter() if self.zoom > 0.5 else None
                    
        self.render()
    
    def setZoomCenter(self):
        self.zoomCenter = ((pygame.Vector2(pygame.mouse.get_pos())-self.zoomCenter)/self.zoom + self.zoomCenter)
        # self.zoomCenter.x = min(max(-50, self.zoomCenter.x), self.rect.width)
        # self.zoomCenter.y = min(max(-50, self.zoomCenter.y), self.rect.width)

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
        self.toolBar = ToolBar(self)
        # Dot(self.canvas)
        Dot(self.canvas, pos=[0, 0])

    def run(self):
        self.active = True
        while self.active:
            self.runEvents()
            self.update()
            self.render()

    def runEvents(self):
        self.clock.tick(FPS)
        self.events = pygame.event.get()
        for event in self.events:
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

