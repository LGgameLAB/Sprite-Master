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

class ToolBar(pygame.sprite.Sprite):
    def __init__(self, editor):
        self.editor = editor
        self.groups = editor.layers.layer0, editor.components
        super().__init__(self.groups)
        self.layers = Layers( [], [], [], [], [], )
        # self.camera = Camera()
        self.components = pygame.sprite.Group()
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
                if scaleRect.colliderect(self.rect):
                    self.image.blit(pygame.transform.scale(i.image, (int(i.image.get_width()*self.zoom), int(i.image.get_height()*self.zoom))), scaleRect)
    
    def update(self):
        self.components.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEWHEEL:
                self.rect.x += 1
            # if event.type == pygame.MOUSEMOTION:
            #     self.zoomCenter = (pygame.Vector2(pygame.mouse.get_pos())-self.zoomCenter)/self.zoom + self.zoomCenter

        print(self.zoomCenter)
        if pygame.mouse.get_pressed(num_buttons=5)[4]:
            self.zoom = min(self.zoom+0.001*deltaConst, 3)
            self.setZoomCenter() if self.zoom < 5 else None

        if pygame.mouse.get_pressed(num_buttons=5)[3]:
            self.zoom = max(self.zoom*0.9992*deltaConst, 0.5)
            self.setZoomCenter() if self.zoom > 0.5 else None
                    
        self.render()
    
    def setZoomCenter(self):
        self.zoomCenter = ((pygame.Vector2(pygame.mouse.get_pos())-self.zoomCenter)/self.zoom + self.zoomCenter)*0.5 +self.zoomCenter*0.5
        self.zoomCenter.x = min(max(0, self.zoomCenter.x), self.rect.width)
        self.zoomCenter.y = min(max(0, self.zoomCenter.y), self.rect.width)

    def scale(self, rect):
        new = pygame.Rect(0, 0, rect.w*self.zoom, rect.h*self.zoom)
        newPos = (1-self.zoom)*pygame.Vector2(self.zoomCenter) + pygame.Vector2(rect.topleft)*self.zoom 
        new.center = newPos
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

