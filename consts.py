import pygame
from enum import Enum
scrren_widht = scrren_height = 720
cell_size = scrren_widht / 15
maxHeightInCells = 14
minHeightInCells = 0
maxWidthInCells = 14
minWidthInCells = 0
freeSpace1 = 6
freeSpace2 = 22
ground = pygame.image.load('images/ground.png')
ground = pygame.transform.scale(ground, (int(cell_size), int(cell_size)))
box = pygame.image.load('images/box.png')
box = pygame.transform.scale(box, (int(cell_size), int(cell_size)))
block = pygame.image.load('images/block.png')
block = pygame.transform.scale(block, (int(cell_size), int(cell_size)))
bombImage = pygame.image.load('images/bomb.png')
bombImage = pygame.transform.scale(bombImage, (int(cell_size * 2), int(cell_size * 2)))
fireImage = pygame.image.load('images/explosion.png')
fireImage = pygame.transform.scale(fireImage, (int(cell_size), int(cell_size)))


class action(Enum):
    bomb = 'bomb'
    left = 'left'
    right = 'right'
    up = 'up'
    down = 'down'


class surface(Enum):
    ground = 1
    box = 2
    block = 3


class directions(Enum):
    up = 0
    down = 1
    right = 2
    left = 3
