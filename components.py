import pygame
from settings import *

class Dot(pygame.sprite.Sprite):
    def __init__(self, editor):
        self.editor = editor
        self.groups = editor.canvas.components, editor.canvas.layers.layer1
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.rect = pygame.Rect(winWidth/3, winHeight/3, 50, 50)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.circle(self.image, orangeRed, (self.rect.w/2, self.rect.h/2), 25)