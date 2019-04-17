from enum import Enum
import consts
import pygame
import random
from pygame import *
pygame.init()
pygame.font.init()

f = pygame.font.Font(None, 20)

scrren_widht = scrren_height = 720
cell_size = scrren_widht / 15
win = pygame.display.set_mode((scrren_widht, scrren_height))


class cell:

    def __init__(self, type):   # 1 - ground, 2 - box, 3 - block
        super().__init__()
        self.type = type
        self.bomb = False
        self.fire = False
        self.size = scrren_height/15
        if type == consts.surface.ground:
            self.image = consts.ground
        elif type == consts.surface.box:
            self.image = consts.box
        elif type == consts.surface.block:
            self.image = consts.block

    def draw(self, x, y):
        global win
        win.blit(self.image, (x, y))
        if self.bomb is True:
            win.blit(consts.bombImage, (x, y))
        elif self.fire is True:
            win.blit(consts.fireImage, (x, y))

    def destroy(self, cellx, celly):
        self.type = consts.surface.ground
        self.image = consts.ground
        self.draw(cellx * self.size, celly * self.size)


class player1:

    def makeDesision(self):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            return consts.action.bomb
        if keys[pygame.K_LEFT]:
            return consts.action.left
        if keys[pygame.K_RIGHT]:
            return consts.action.right
        if keys[pygame.K_UP]:
            return consts.action.up
        if keys[pygame.K_DOWN]:
            return consts.action.down


class player2:
    def makeDesision(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            return consts.action.bomb
        if keys[pygame.K_a]:
            return consts.action.left
        if keys[pygame.K_d]:
            return consts.action.right
        if keys[pygame.K_w]:
            return consts.action.up
        if keys[pygame.K_s]:
            return consts.action.down


class unit:
    force: int = 3
    bomb: int = 3
    speed: int = 16
    health: int = 4

    def __init__(self, manager, map, direction):
        super().__init__()
        self.direction = consts.directions.down
        self.map = map
        self.manager = manager
        self.x = 10
        self.y = 10
        self.walkDown = pygame.image.load('images/tile_0267.png')
        self.walkDown = pygame.transform.scale(self.walkDown, (int(cell_size), \
        int(cell_size)))

    def damage(self):
        self.health -= 1

    def moveUp(self):
        if self.direction != consts.directions.up:
            self.direction = consts.directions.up
        else:
            self.map.moveUp(self)

    def moveDown(self):
        if self.direction != consts.directions.down:
            self.direction = consts.directions.down
        else:
            self.map.moveDown(self)

    def moveLeft(self):
        if self.direction != consts.directions.left:
            self.direction = consts.directions.left
        else:
            self.map.moveLeft(self)

    def moveRight(self):
        if self.direction != consts.directions.right:
            self.direction = consts.directions.right
        else:
            self.map.moveRight(self)

    def performAnAction(self):
        decision = self.manager.makeDesision()
        if decision == consts.action.bomb and self.bomb > 0:
            self.bomb -= 1
            self.map.pickBomb(self.x, self.y, self.force, self)
        if decision == consts.action.up:
            self.moveUp()
        if decision == consts.action.down:
            self.moveDown()
        if decision == consts.action.left:
            self.moveLeft()
        if decision == consts.action.right:
            self.moveRight()


class map:

    mapMatrix = list()

    def __init__(self, units = list()):
        super().__init__()
        self.bombs = list()
        self.addBombs = list()
        self.fire = list()
        self.units = units
        mapMatrix = list()
        for i in range(15):
            tmp = list()
            for j in range(15):
                if i == consts.minHeightInCells or \
                j == consts.minWidthInCells or i == consts.maxHeightInCells or \
                j == consts.maxWidthInCells or ((i % 2 == 0) and \
                (j % 2 == 0) and i != consts.maxHeightInCells and \
                j != consts.minWidthInCells and \
                i != consts.maxWidthInCells and j != consts.maxHeightInCells):
                    new_cell = cell(consts.surface.block)
                elif i + j < consts.freeSpace1 or i + j > consts.freeSpace2:
                    new_cell = cell(consts.surface.ground)
                else:
                    new_cell = cell(consts.surface.box)
                tmp.append(new_cell)
            mapMatrix.append(tmp)
            self.mapMatrix = mapMatrix

    def destroyCell(self, cellx, celly):
        self.mapMatrix[cellx][celly].destroy(cellx, celly)

    def getCellXYByXY(self, x, y):
        return int(x // cell_size), int(y // cell_size)

    def drawCurrMap(self):
        for i in range(len(self.mapMatrix)):
            for j in range(len(self.mapMatrix[i])):
                self.mapMatrix[i][j].draw(i * self.mapMatrix[i][j].size, j * \
                self.mapMatrix[i][j].size)

    def moveUp(self, unit):
        cellx, celly = self.getCellXYByXY(unit.x, unit.y)
        up = self.whereIsAvailable(unit.x, unit.y)[0]
        if up == 1 and unit.x % cell_size == cell_size / 2:
            unit.y -= unit.speed
        elif up == 1 and unit.x % cell_size < cell_size / 2:
            unit.x += unit.speed
        elif up == 1 and unit.x % cell_size > cell_size / 2:
            unit.x -= unit.speed
        elif unit.x % cell_size > cell_size // 2:
            if self.mapMatrix[cellx + 1][celly - 1].type == \
            consts.surface.ground and \
            self.mapMatrix[cellx + 1][celly].type == consts.surface.ground:
                unit.x += unit.speed
        elif self.mapMatrix[cellx - 1][celly - 1].type == \
        consts.surface.ground and \
        self.mapMatrix[cellx - 1][celly].type == consts.surface.ground:
            unit.x -= unit.speed

    def moveDown(self, unit):
        cellx, celly = self.getCellXYByXY(unit.x, unit.y)
        down = self.whereIsAvailable(unit.x, unit.y)[1]
        if down == 1 and unit.x % cell_size == cell_size / 2:
            unit.y += unit.speed
        elif down == 1 and unit.x % cell_size < cell_size / 2:
            unit.x += unit.speed
        elif down == 1 and unit.x % cell_size > cell_size / 2:
            unit.x -= unit.speed
        elif unit.x % cell_size > cell_size // 2:
            if self.mapMatrix[cellx + 1][celly + 1].type == \
            consts.surface.ground and \
            self.mapMatrix[cellx + 1][celly].type == consts.surface.ground:
                unit.x += unit.speed
        elif self.mapMatrix[cellx - 1][celly + 1].type == \
        consts.surface.ground and \
        self.mapMatrix[cellx - 1][celly].type == consts.surface.ground:
            unit.x -= unit.speed

    def moveRight(self, unit):
        cellx, celly = self.getCellXYByXY(unit.x, unit.y)
        right = self.whereIsAvailable(unit.x, unit.y)[2]
        if right == 1 and unit.y % cell_size == cell_size / 2:
            unit.x += unit.speed
        elif right == 1 and unit.y % cell_size < cell_size / 2:
            unit.y += unit.speed
        elif right == 1 and unit.y % cell_size > cell_size / 2:
            unit.y -= unit.speed
        elif unit.y % cell_size > cell_size // 2:
            if self.mapMatrix[cellx + 1][celly + 1].type == \
            consts.surface.ground and \
            self.mapMatrix[cellx][celly + 1].type == consts.surface.ground:
                unit.y += unit.speed
        elif self.mapMatrix[cellx + 1][celly - 1].type == \
        consts.surface.ground and self.mapMatrix[cellx][celly - 1].type == \
        consts.surface.ground:
            unit.y -= unit.speed

    def moveLeft(self, unit):
        cellx, celly = self.getCellXYByXY(unit.x, unit.y)
        left = self.whereIsAvailable(unit.x, unit.y)[3]
        if left == 1 and unit.y % cell_size == cell_size / 2:
            unit.x -= unit.speed
        elif left == 1 and unit.y % cell_size < cell_size / 2:
            unit.y += unit.speed
        elif left == 1 and unit.y % cell_size > cell_size / 2:
            unit.y -= unit.speed
        elif unit.y % cell_size > cell_size // 2:
            if self.mapMatrix[cellx - 1][celly + 1].type == \
            consts.surface.ground and \
            self.mapMatrix[cellx][celly + 1].type == consts.surface.ground:
                unit.y += unit.speed
        elif self.mapMatrix[cellx - 1][celly - 1].type == \
        consts.surface.ground and \
        self.mapMatrix[cellx][celly - 1].type == consts.surface.ground:
            unit.y -= unit.speed

    def drawUnits(self):
        global win
        for unit in self.units:
            self.drawUnit(unit)

    def drawUnit(self, unit):
        win.blit(unit.walkDown,
                 (unit.x - unit.walkDown.get_width() // 2, \
                 unit.y - unit.walkDown.get_height() // 2))

    def whereIsAvailable(self, x, y):
        cellx, celly = self.getCellXYByXY(x, y)
        print(cellx, celly)
        avalibility = [0, 0, 0, 0]  # UP, DOWN, RIGHT, LEFT
        if celly != consts.maxHeightInCells and \
        (self.mapMatrix[cellx][celly-1].type == consts.surface.ground or \
        y % cell_size != cell_size / 2):
            avalibility[0] = 1
        if celly != consts.maxHeightInCells and \
        (self.mapMatrix[cellx][celly+1].type == consts.surface.ground or \
        y % cell_size != cell_size / 2):
            avalibility[1] = 1
        if cellx != consts.maxHeightInCells and \
        (self.mapMatrix[cellx+1][celly].type == consts.surface.ground or \
        x % cell_size != cell_size / 2):
            avalibility[2] = 1
        if cellx != consts.minHeightInCells and \
        (self.mapMatrix[cellx-1][celly].type == consts.surface.ground or \
        x % cell_size != cell_size / 2):
            avalibility[3] = 1
        return avalibility

    def pickBomb(self, x, y, force, unit):
        now = pygame.time.get_ticks()
        cellx, celly = self.getCellXYByXY(x, y)
        self.bombs.append((cellx, celly, force, now))
        self.addBombs.append((unit, now))
        self.mapMatrix[cellx][celly].bomb = True
        self.mapMatrix[cellx][celly].fire = True

    def dellBomb(self, cellx, celly):
        self.mapMatrix[cellx][celly].bomb = False

    def dellFire(self, cellx, celly):
        self.mapMatrix[cellx][celly].fire = False

    def explosion(self, cellx, celly, force):
        now = pygame.time.get_ticks()
        for u in units:
            cellx1, celly1 = self.getCellXYByXY(u.x, u.y)
            for i in range(force):
                if self.mapMatrix[cellx][celly + i].type == consts.surface.block:
                    break
                self.mapMatrix[cellx][celly + i].fire = True
                self.fire.append((cellx, celly + i, now))
                self.destroyCell(cellx, celly + i)
                if cellx == cellx1 and celly + i == celly1:
                    u.damage()
            for i in range(force):
                if self.mapMatrix[cellx][celly - i].type == consts.surface.block:
                    break
                self.mapMatrix[cellx][celly - i].fire = True
                self.fire.append((cellx, celly - i, now))
                self.destroyCell(cellx, celly - i)
                if cellx == cellx1 and celly - i == celly1:
                    u.damage()
            for i in range(force):
                if self.mapMatrix[cellx + i][celly].type == consts.surface.block:
                    break
                self.mapMatrix[cellx + i][celly].fire = True
                self.fire.append((cellx + i, celly, now))
                self.destroyCell(cellx + i, celly)
                if cellx + i == cellx1 and celly == celly1:
                        u.damage()
            for i in range(force):
                if self.mapMatrix[cellx - i][celly].type == consts.surface.block:
                    break
                self.mapMatrix[cellx - i][celly].fire = True
                self.fire.append((cellx - i, celly, now))
                self.destroyCell(cellx - i, celly)
                if cellx - i == cellx1 and celly == celly1:
                        u.damage()
if __name__ == '__main__':
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

        if len(mapx.bombs) != 0 and pygame.time.get_ticks() - \
        mapx.bombs[0][3] > 1500:
            mapx.explosion(mapx.bombs[0][0], mapx.bombs[0][1], mapx.bombs[0][2])
            mapx.dellBomb(mapx.bombs[0][0], mapx.bombs[0][1])
            del mapx.bombs[0]
        if len(mapx.addBombs) != 0 and pygame.time.get_ticks() - \
        mapx.addBombs[0][1] > 1500:
            mapx.addBombs[0][0].bomb += 1
            del mapx.addBombs[0]
        if len(mapx.fire) != 0 and pygame.time.get_ticks() - \
        mapx.fire[0][2] > 200:
            mapx.dellFire(mapx.fire[0][0], mapx.fire[0][1])
            del mapx.fire[0]
        mapx.drawCurrMap()
        mapx.drawUnits()
        for u in units:
            if u.health <= 0:
                run = False
        c1 = f.render("Health of player1:{}".format(unit1.health), True, \
        [0, 0, 0], [255, 255, 255])
        c2 = f.render("Health of player2:{}".format(unit2.health), True, \
        [0, 0, 0], [255, 255, 255])
        win.blit(c1, (20, 10))
        win.blit(c2, (20, 24))
        pygame.display.update()
    pygame.quit()
