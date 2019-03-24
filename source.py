import pygame
import random
from pygame import *
pygame.init()
pygame.font.init()

f = pygame.font.Font(None, 20)

scrren_widht = scrren_height = 720
cell_size = scrren_widht / 15
win = pygame.display.set_mode((scrren_widht, scrren_height))

ground = pygame.image.load('ground.png')
ground = pygame.transform.scale(ground, (int(cell_size), int(cell_size)))
box = pygame.image.load('box.png')
box = pygame.transform.scale(box, (int(cell_size), int(cell_size)))
block = pygame.image.load('block.png')
block = pygame.transform.scale(block, (int(cell_size), int(cell_size)))
bombImage = pygame.image.load('bomb.png')
bombImage = pygame.transform.scale(bombImage, (int(cell_size*2), int(cell_size*2)))
fireImage = pygame.image.load('explosion.png')
fireImage = pygame.transform.scale(fireImage, (int(cell_size), int(cell_size)))
class cell:
    global ground, box, block, fireImage, bombImage

    def __init__(self, type): # 1 - ground, 2 - box, 3 - block
        self.type = type
        self.bomb = False
        self.fire = False
        self.size = scrren_height/15
        if type == 1:
            self.image = ground
        elif type == 2:
            self.image = box
        elif type == 3:
            self.image = block



    def draw(self, x, y):
        global win
        win.blit(self.image, (x, y))
        if self.bomb == True:
            win.blit(bombImage, (x, y))
        elif self.fire == True:
            win.blit(fireImage, (x, y))


    def destroy(self, cellx, celly):
        self.type = 1
        self.image = ground
        self.draw(cellx * self.size, celly * self.size)
class AI:
    def makeDesision(self):
        pass
class player1:
    def makeDesision(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            return 'bomb'
        if keys[pygame.K_LEFT]:
            return 'left'
        if keys[pygame.K_RIGHT]:
            return 'right'
        if keys[pygame.K_UP]:
            return 'up'
        if keys[pygame.K_DOWN]:
            return 'down'

class player2:
    def makeDesision(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            return 'bomb'
        if keys[pygame.K_a]:
            return 'left'
        if keys[pygame.K_d]:
            return 'right'
        if keys[pygame.K_w]:
            return 'up'
        if keys[pygame.K_s]:
            return 'down'

class unit:
    direction: int = 0
    force: int = 3
    bomb: int = 3
    speed: int = 16
    health: int = 4
    def __init__(self, manager, map, direction):
        self.direction = direction
        self.map = map
        self.manager = manager
        self.x = 10
        self.y = 10

        self.walkRight = [pygame.image.load('tile_0269.png'),
                     pygame.image.load('tile_0296.png'),]

        self.walkLeft = [pygame.image.load('tile_0266.png'),
                    pygame.image.load('tile_0293.png'),]

        self.walkUp = [pygame.image.load('tile_0268.png'),
                     pygame.image.load('tile_0295.png'), ]

        self.walkDown = [pygame.image.load('tile_0267.png'),
                    pygame.image.load('tile_0294.png'), ]
        for i in [self.walkDown, self.walkLeft, self.walkRight, self.walkUp]:
            #print(i)
            for j in range(2):
                #print(j)
                i[j] = pygame.transform.scale(i[j], (int(cell_size), int(cell_size)))
                #print('>>>>', j)
    def moveUp(self):
        if self.direction != 'up':
            self.direction = 'up'
        else:
            self.map.moveUp(self)

    def moveDown(self):
        if self.direction != 'down':
            self.direction = 'down'
        else:
            self.map.moveDown(self)


    def moveLeft(self):
        if self.direction != 'left':
            self.direction = 'left'
        else:
            self.map.moveLeft(self)


    def moveRight(self):
        if self.direction != 'right':
            self.direction = 'right'
        else:
            self.map.moveRight(self)


    def performAnAction(self):
        desisison = self.manager.makeDesision()
        if desisison == 'bomb' and self.bomb > 0:
            self.bomb -= 1
            self.map.pickBomb(self.x, self.y, self.force, self)
        if desisison == 'up':
            self.moveUp()
        if desisison == 'down':
            self.moveDown()
        if desisison == 'left':
            self.moveLeft()
        if desisison == 'right':
            self.moveRight()




class map:


    mapMatrix = list()
    def __init__(self, units = list()):
        self.bombs = list()
        self.addBombs = list()
        self.fire = list()
        self.units = units
        mapMatrix = list()
        for i in range(15):
            tmp = list()
            for j in range(15):
                if i == 0 or j == 0 or i == 14 or j == 14 or ((i % 2 == 0 ) and (j % 2 == 0) and i!= 0 and j!= 0 and i!=14 and j!= 14):
                    new_cell = cell(3)
                elif i + j < 6 or i + j > 22:
                    new_cell = cell(1)
                else:
                    new_cell = cell(2)
                tmp.append(new_cell)
            mapMatrix.append(tmp)
            self.mapMatrix = mapMatrix


    def destroyCell(self, cellx, celly):
        self.mapMatrix[cellx][celly].destroy(cellx, celly)


    def getCellXYByXY(self, x, y):
        return int(x // cell_size), int(y // cell_size)


    def drawCurrMap(self):
        for i in  range(len(self.mapMatrix)):
            for j in range(len(self.mapMatrix[i])):
                self.mapMatrix[i][j].draw(i * self.mapMatrix[i][j].size, j * self.mapMatrix[i][j].size)

    def moveUp(self, unit):
        cellx, celly = self.getCellXYByXY(unit.x, unit.y)
        #print(unit.manager, cellx, celly)
        if self.whereIsAvailable(unit.x, unit.y)[0] == 1 and unit.x % cell_size == cell_size / 2:
            unit.y -= unit.speed
        elif self.whereIsAvailable(unit.x, unit.y)[0] == 1 and unit.x % cell_size < cell_size / 2:
            unit.x += unit.speed
        elif self.whereIsAvailable(unit.x, unit.y)[0] == 1 and unit.x % cell_size > cell_size / 2:
            unit.x -= unit.speed
        elif unit.x % cell_size > cell_size // 2:
            if self.mapMatrix[cellx + 1][celly - 1].type == 1 and self.mapMatrix[cellx + 1][celly].type == 1:
                unit.x += unit.speed
        elif self.mapMatrix[cellx - 1][celly - 1].type == 1 and self.mapMatrix[cellx - 1][celly].type == 1:
            unit.x -= unit.speed

    def moveDown(self, unit):
        cellx, celly = self.getCellXYByXY(unit.x, unit.y)
        if self.whereIsAvailable(unit.x, unit.y)[1] == 1 and unit.x % cell_size == cell_size / 2:
            unit.y += unit.speed
        elif self.whereIsAvailable(unit.x, unit.y)[1] == 1 and unit.x % cell_size < cell_size / 2:
            unit.x += unit.speed
        elif self.whereIsAvailable(unit.x, unit.y)[1] == 1 and unit.x % cell_size > cell_size / 2:
            unit.x -= unit.speed
        elif unit.x % cell_size > cell_size // 2:
           # print(cellx, celly)
            if self.mapMatrix[cellx + 1][celly + 1].type == 1 and self.mapMatrix[cellx + 1][celly].type == 1:
                unit.x += unit.speed
        elif self.mapMatrix[cellx - 1][celly + 1].type == 1 and self.mapMatrix[cellx - 1][celly].type == 1:
            unit.x -= unit.speed


    def moveRight(self, unit):
        cellx, celly = self.getCellXYByXY(unit.x, unit.y)
        if self.whereIsAvailable(unit.x, unit.y)[2] == 1 and unit.y % cell_size == cell_size / 2:
            unit.x += unit.speed
        elif self.whereIsAvailable(unit.x, unit.y)[2] == 1 and unit.y % cell_size < cell_size / 2:
            unit.y += unit.speed
        elif self.whereIsAvailable(unit.x, unit.y)[2] == 1 and unit.y % cell_size > cell_size / 2:
            unit.y -= unit.speed
        elif unit.y % cell_size > cell_size // 2:
            if self.mapMatrix[cellx + 1][celly + 1].type == 1 and self.mapMatrix[cellx][celly + 1].type == 1:
                unit.y += unit.speed
        elif self.mapMatrix[cellx + 1][celly - 1].type == 1 and self.mapMatrix[cellx][celly - 1].type == 1:
            unit.y -= unit.speed

    def moveLeft(self, unit):
        cellx, celly = self.getCellXYByXY(unit.x, unit.y)
        if self.whereIsAvailable(unit.x, unit.y)[3] == 1 and unit.y % cell_size == cell_size / 2:
            unit.x -= unit.speed
        elif self.whereIsAvailable(unit.x, unit.y)[3] == 1 and unit.y % cell_size < cell_size / 2:
            unit.y += unit.speed
        elif self.whereIsAvailable(unit.x, unit.y)[3] == 1 and unit.y % cell_size > cell_size / 2:
            unit.y -= unit.speed
        elif unit.y % cell_size > cell_size // 2:
            if self.mapMatrix[cellx - 1][celly + 1].type == 1 and self.mapMatrix[cellx][celly + 1].type == 1:
                unit.y += unit.speed
        elif self.mapMatrix[cellx - 1][celly - 1].type == 1 and self.mapMatrix[cellx][celly - 1].type == 1:
            unit.y -= unit.speed


    def drawUnits(self):
        global win
        for unit in self.units:
            self.drawUnit(unit)



    def drawUnit(self, unit):
        #unit.walkDown: list(pygame.image)
        win.blit(unit.walkDown[0],
                 (unit.x - unit.walkDown[0].get_width() // 2, unit.y - unit.walkDown[0].get_height() // 2))

    def whereIsAvailable(self,x, y):
        cellx, celly = self.getCellXYByXY(x, y)
        avalibility = [0, 0, 0, 0] # UP, DOWN, RIGHT, LEFT
        if celly != 0 and ( self.mapMatrix[cellx][celly-1].type == 1 or y % cell_size != cell_size / 2):
            avalibility[0] =  1
        if celly != 14 and ( self.mapMatrix[cellx][celly+1].type == 1 or y % cell_size != cell_size / 2):
            avalibility[1] = 1
        if cellx != 14 and ( self.mapMatrix[cellx+1][celly].type == 1 or x % cell_size != cell_size / 2):
            avalibility[2]= 1
        if cellx != 0 and ( self.mapMatrix[cellx-1][celly].type == 1 or x % cell_size != cell_size / 2):
            avalibility[3]= 1
        return avalibility


    def pickBomb(self, x, y, force, unit):
        print(dir(unit))
        now = pygame.time.get_ticks()
        cellx, celly = self.getCellXYByXY(x, y)
        self.bombs.append((cellx, celly, force, now))
        self.addBombs.append((unit, now))
        self.mapMatrix[cellx][celly].bomb = True
        self.mapMatrix[cellx][celly].fire = True
        #print(self.fire)


    def dellBomb(self, cellx, celly):
        self.mapMatrix[cellx][celly].bomb = False


    def dellFire(self, cellx, celly):
        self.mapMatrix[cellx][celly].fire = False

    def explosion(self, cellx, celly, force):
        now = pygame.time.get_ticks()
        for u in units:
            cellx1, celly1 = self.getCellXYByXY(u.x, u.y)
            for i in range(force):
                if self.mapMatrix[cellx][celly + i].type != 3:
                    self.mapMatrix[cellx][celly + i].fire = True
                    self.fire.append((cellx, celly + i, now))
                    self.destroyCell(cellx, celly + i)
                    if cellx == cellx1 and celly + i == celly1:
                        u.health -=1

                else:
                    break
            for i in range(force):
                if self.mapMatrix[cellx][celly - i].type != 3:
                    self.mapMatrix[cellx][celly - i].fire = True
                    self.fire.append((cellx, celly - i, now))
                    self.destroyCell(cellx, celly - i)
                    if cellx == cellx1 and celly - i == celly1:
                        u.health -= 1
                else:
                    break
            for i in range(force):
                if self.mapMatrix[cellx + i][celly].type != 3:
                    self.mapMatrix[cellx + i][celly].fire = True
                    self.fire.append((cellx + i, celly, now))
                    self.destroyCell(cellx + i, celly)
                    if cellx + i== cellx1 and celly == celly1:
                            u.health -= 1
                else:
                    break
            for i in range(force):
                if self.mapMatrix[cellx - i][celly].type != 3:
                    self.mapMatrix[cellx - i][celly].fire = True
                    self.fire.append((cellx - i, celly, now))
                    self.destroyCell(cellx - i, celly)
                    if cellx - i == cellx1 and celly == celly1:
                            u.health -= 1
                else:
                    break

pygame.display.set_caption("BomberMan")
x = 0.5*cell_size
y = 0.5*cell_size
widht = 40
heigth = 60
speed = 15

run = True

player1 = player1()
player2 = player2()
units = list()
mapx = map()
unit1 = unit(player1, mapx, 'down')
unit2 = unit(player2, mapx, 'down')
unit1.x = int(1.5*cell_size)
unit1.y = int(1.5*cell_size)
unit2.x = int(scrren_widht - 1.5*cell_size)
unit2.y = int(scrren_height - 1.5*cell_size)
units.append(unit1)
units.append(unit2)
mapx.units = units
while run:
    pygame.time.delay(15)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    unit1.performAnAction()
    unit2.performAnAction()

    if len(mapx.bombs) != 0 and pygame.time.get_ticks() - mapx.bombs[0][3] > 1500:
        mapx.explosion(mapx.bombs[0][0], mapx.bombs[0][1], mapx.bombs[0][2])
        mapx.dellBomb(mapx.bombs[0][0], mapx.bombs[0][1])
        del mapx.bombs[0]
    if len(mapx.addBombs) != 0 and pygame.time.get_ticks() - mapx.addBombs[0][1] > 1500:
        mapx.addBombs[0][0].bomb += 1
        del mapx.addBombs[0]
    if len(mapx.fire) != 0 and pygame.time.get_ticks() - mapx.fire[0][2] > 200:
        print(mapx.fire)
        mapx.dellFire(mapx.fire[0][0], mapx.fire[0][1])
        del mapx.fire[0]
    mapx.drawCurrMap()
    mapx.drawUnits()
    for u in units:
        if u.health <= 0:
            run = False
    c1 = f.render("Health of player1:{}".format(unit1.health), True, [0,0,0], [255, 255, 255])
    c2 = f.render("Health of player2:{}".format(unit2.health), True, [0, 0, 0], [255, 255, 255])
    win.blit(c1, (20, 10))
    win.blit(c2, (20, 24))
    pygame.display.update()
pygame.quit()




