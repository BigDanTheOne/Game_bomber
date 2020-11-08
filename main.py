from enum import Enum
import consts
import pygame
import random
from pygame import *
from consts import *
pygame.init()
pygame.font.init()


class Cell:

    def __init__(self, type):   # 1 - ground, 2 - box, 3 - block
        super().__init__()
        self.type = type
        self.bomb = False
        self.fire = False
        self.size = scrren_height/15
        if type == consts.Surface.ground:
            self.image = consts.ground
        elif type == consts.Surface.box:
            self.image = consts.box
        elif type == consts.Surface.block:
            self.image = consts.block

    def draw(self, x, y):
        global win
        win.blit(self.image, (x, y))
        if self.bomb is True:
            win.blit(consts.bombImage, (x, y))
        elif self.fire is True:
            win.blit(consts.fireImage, (x, y))

    def destroy(self, cell_x, cell_y):
        self.type = consts.Surface.ground
        self.image = consts.ground
        self.draw(cell_x * self.size, cell_y * self.size)


class Player1:

    def make_desision(self):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            return consts.Action.bomb
        if keys[pygame.K_LEFT]:
            return consts.Action.left
        if keys[pygame.K_RIGHT]:
            return consts.Action.right
        if keys[pygame.K_UP]:
            return consts.Action.up
        if keys[pygame.K_DOWN]:
            return consts.Action.down


class Player2:
    def make_desision(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            return consts.Action.bomb
        if keys[pygame.K_a]:
            return consts.Action.left
        if keys[pygame.K_d]:
            return consts.Action.right
        if keys[pygame.K_w]:
            return consts.Action.up
        if keys[pygame.K_s]:
            return consts.Action.down


class Unit:
    force: int = 3
    bomb: int = 3
    speed: int = 16
    health: int = 4

    def __init__(self, manager, map, direction):
        super().__init__()
        self.direction = consts.Directions.down
        self.map = map
        self.manager = manager
        self.x = 10
        self.y = 10
        self.walkDown = pygame.image.load('images/tile_0267.png')
        self.walkDown = pygame.transform.scale(self.walkDown, (int(cell_size), \
        int(cell_size)))

    def damage(self):
        self.health -= 1

    def move_up(self):
        if self.direction != consts.Directions.up:
            self.direction = consts.Directions.up
        else:
            self.map.move_up(self)

    def move_down(self):
        if self.direction != consts.Directions.down:
            self.direction = consts.Directions.down
        else:
            self.map.move_down(self)

    def move_left(self):
        if self.direction != consts.Directions.left:
            self.direction = consts.Directions.left
        else:
            self.map.move_left(self)

    def move_right(self):
        if self.direction != consts.Directions.right:
            self.direction = consts.Directions.right
        else:
            self.map.move_right(self)

    def perform_an_action(self):
        decision = self.manager.make_desision()
        if decision == consts.Action.bomb and self.bomb > 0:
            self.bomb -= 1
            self.map.pick_bomb(self.x, self.y, self.force, self)
        if decision == consts.Action.up:
            self.move_up()
        if decision == consts.Action.down:
            self.move_down()
        if decision == consts.Action.left:
            self.move_left()
        if decision == consts.Action.right:
            self.move_right()


class Map:

    def __init__(self, units = list()):
        super().__init__()
        self.bombs = list()
        self.addBombs = list()
        self.fire = list()
        self.units = units
        map_matrix = list()
        for i in range(15):
            tmp = list()
            for j in range(15):
                if i == consts.minHeightInCells or \
                j == consts.minWidthInCells or i == consts.maxHeightInCells or \
                j == consts.maxWidthInCells or ((i % 2 == 0) and \
                (j % 2 == 0) and i != consts.maxHeightInCells and \
                j != consts.minWidthInCells and \
                i != consts.maxWidthInCells and j != consts.maxHeightInCells):
                    new_cell = Cell(consts.Surface.block)
                elif i + j < consts.freeSpace1 or i + j > consts.freeSpace2:
                    new_cell = Cell(consts.Surface.ground)
                else:
                    new_cell = Cell(consts.Surface.box)
                tmp.append(new_cell)
            map_matrix.append(tmp)
            self.map_matrix = map_matrix

    def destroy_cell(self, cell_x, cell_y):
        self.map_matrix[cell_x][cell_y].destroy(cell_x, cell_y)

    def getcell_xy_by_yx(self, x, y):
        return int(x // cell_size), int(y // cell_size)

    def draw_curr_map(self):
        for i in range(len(self.map_matrix)):
            for j in range(len(self.map_matrix[i])):
                self.map_matrix[i][j].draw(i * self.map_matrix[i][j].size, j * self.map_matrix[i][j].size)

    def move_up(self, unit):
        cell_x, cell_y = self.getcell_xy_by_yx(unit.x, unit.y)
        up = self.where_is_available(unit.x, unit.y)[0]
        if up == 1 and unit.x % cell_size == cell_size / 2:
            unit.y -= unit.speed
        elif up == 1 and unit.x % cell_size < cell_size / 2:
            unit.x += unit.speed
        elif up == 1 and unit.x % cell_size > cell_size / 2:
            unit.x -= unit.speed
        elif unit.x % cell_size > cell_size // 2:
            if self.map_matrix[cell_x + 1][cell_y - 1].type == \
            consts.Surface.ground and \
            self.map_matrix[cell_x + 1][cell_y].type == consts.Surface.ground:
                unit.x += unit.speed
        elif self.map_matrix[cell_x - 1][cell_y - 1].type == \
        consts.Surface.ground and \
        self.map_matrix[cell_x - 1][cell_y].type == consts.Surface.ground:
            unit.x -= unit.speed

    def move_down(self, unit):
        cell_x, cell_y = self.getcell_xy_by_yx(unit.x, unit.y)
        down = self.where_is_available(unit.x, unit.y)[1]
        if down == 1 and unit.x % cell_size == cell_size / 2:
            unit.y += unit.speed
        elif down == 1 and unit.x % cell_size < cell_size / 2:
            unit.x += unit.speed
        elif down == 1 and unit.x % cell_size > cell_size / 2:
            unit.x -= unit.speed
        elif unit.x % cell_size > cell_size // 2:
            if self.map_matrix[cell_x + 1][cell_y + 1].type == \
            consts.Surface.ground and \
            self.map_matrix[cell_x + 1][cell_y].type == consts.Surface.ground:
                unit.x += unit.speed
        elif self.map_matrix[cell_x - 1][cell_y + 1].type == \
        consts.Surface.ground and \
        self.map_matrix[cell_x - 1][cell_y].type == consts.Surface.ground:
            unit.x -= unit.speed

    def move_right(self, unit):
        cell_x, cell_y = self.getcell_xy_by_yx(unit.x, unit.y)
        right = self.where_is_available(unit.x, unit.y)[2]
        if right == 1 and unit.y % cell_size == cell_size / 2:
            unit.x += unit.speed
        elif right == 1 and unit.y % cell_size < cell_size / 2:
            unit.y += unit.speed
        elif right == 1 and unit.y % cell_size > cell_size / 2:
            unit.y -= unit.speed
        elif unit.y % cell_size > cell_size // 2:
            if self.map_matrix[cell_x + 1][cell_y + 1].type == \
            consts.Surface.ground and \
            self.map_matrix[cell_x][cell_y + 1].type == consts.Surface.ground:
                unit.y += unit.speed
        elif self.map_matrix[cell_x + 1][cell_y - 1].type == \
        consts.Surface.ground and self.map_matrix[cell_x][cell_y - 1].type == \
        consts.Surface.ground:
            unit.y -= unit.speed

    def move_left(self, unit):
        cell_x, cell_y = self.getcell_xy_by_yx(unit.x, unit.y)
        left = self.where_is_available(unit.x, unit.y)[3]
        if left == 1 and unit.y % cell_size == cell_size / 2:
            unit.x -= unit.speed
        elif left == 1 and unit.y % cell_size < cell_size / 2:
            unit.y += unit.speed
        elif left == 1 and unit.y % cell_size > cell_size / 2:
            unit.y -= unit.speed
        elif unit.y % cell_size > cell_size // 2:
            if self.map_matrix[cell_x - 1][cell_y + 1].type == \
            consts.Surface.ground and \
            self.map_matrix[cell_x][cell_y + 1].type == consts.Surface.ground:
                unit.y += unit.speed
        elif self.map_matrix[cell_x - 1][cell_y - 1].type == \
        consts.Surface.ground and \
        self.map_matrix[cell_x][cell_y - 1].type == consts.Surface.ground:
            unit.y -= unit.speed

    def draw_units(self):
        global win
        for unit in self.units:
            self.draw_unit(unit)

    def draw_unit(self, unit):
        win.blit(unit.walkDown,
                 (unit.x - unit.walkDown.get_width() // 2, \
                 unit.y - unit.walkDown.get_height() // 2))

    def where_is_available(self, x, y):
        cell_x, cell_y = self.getcell_xy_by_yx(x, y)
      
        avalibility = [0, 0, 0, 0]  # UP, DOWN, RIGHT, LEFT
        if cell_y != consts.maxHeightInCells and \
        (self.map_matrix[cell_x][cell_y-1].type == consts.Surface.ground or \
         y % cell_size != cell_size / 2):
            avalibility[0] = 1
        if cell_y != consts.maxHeightInCells and \
        (self.map_matrix[cell_x][cell_y+1].type == consts.Surface.ground or \
         y % cell_size != cell_size / 2):
            avalibility[1] = 1
        if cell_x != consts.maxHeightInCells and \
        (self.map_matrix[cell_x+1][cell_y].type == consts.Surface.ground or \
         x % cell_size != cell_size / 2):
            avalibility[2] = 1
        if cell_x != consts.minHeightInCells and \
        (self.map_matrix[cell_x-1][cell_y].type == consts.Surface.ground or \
         x % cell_size != cell_size / 2):
            avalibility[3] = 1
        return avalibility

    def pick_bomb(self, x, y, force, unit):
        now = pygame.time.get_ticks()
        cell_x, cell_y = self.getcell_xy_by_yx(x, y)
        self.bombs.append((cell_x, cell_y, force, now))
        self.addBombs.append((unit, now))
        self.map_matrix[cell_x][cell_y].bomb = True
        self.map_matrix[cell_x][cell_y].fire = True

    def dell_bomb(self, cell_x, cell_y):
        self.map_matrix[cell_x][cell_y].bomb = False

    def dell_fire(self, cell_x, cell_y):
        self.map_matrix[cell_x][cell_y].fire = False

    def explosion(self, cell_x, cell_y, force):
        now = pygame.time.get_ticks()
        for u in units:
            cell_x_1, cell_y_1 = self.getcell_xy_by_yx(u.x, u.y)
            for i in range(force):
                if self.map_matrix[cell_x][cell_y + i].type == consts.Surface.block:
                    break
                self.map_matrix[cell_x][cell_y + i].fire = True
                self.fire.append((cell_x, cell_y + i, now))
                self.destroy_cell(cell_x, cell_y + i)
                if cell_x == cell_x_1 and cell_y + i == cell_y_1:
                    u.damage()
            for i in range(force):
                if self.map_matrix[cell_x][cell_y - i].type == consts.Surface.block:
                    break
                self.map_matrix[cell_x][cell_y - i].fire = True
                self.fire.append((cell_x, cell_y - i, now))
                self.destroy_cell(cell_x, cell_y - i)
                if cell_x == cell_x_1 and cell_y - i == cell_y_1:
                    u.damage()
            for i in range(force):
                if self.map_matrix[cell_x + i][cell_y].type == consts.Surface.block:
                    break
                self.map_matrix[cell_x + i][cell_y].fire = True
                self.fire.append((cell_x + i, cell_y, now))
                self.destroy_cell(cell_x + i, cell_y)
                if cell_x + i == cell_x_1 and cell_y == cell_y_1:
                        u.damage()
            for i in range(force):
                if self.map_matrix[cell_x - i][cell_y].type == consts.Surface.block:
                    break
                self.map_matrix[cell_x - i][cell_y].fire = True
                self.fire.append((cell_x - i, cell_y, now))
                self.destroy_cell(cell_x - i, cell_y)
                if cell_x - i == cell_x_1 and cell_y == cell_y_1:
                        u.damage()


class Game:
    run = True
    mapx = Map()
    Player1 = Player1()
    Player2 = Player2()
    unit1 = Unit(Player1, mapx, 'down')
    unit2 = Unit(Player2, mapx, 'down')
    unit1.x = int(1.5 * cell_size)
    unit1.y = int(1.5 * cell_size)
    unit2.x = int(scrren_widht - 1.5 * cell_size)
    unit2.y = int(scrren_height - 1.5 * cell_size)
    units.append(unit1)
    units.append(unit2)
    mapx.units = units
    def play(self):
        while self.run:
            pygame.time.delay(15)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

            self.unit1.perform_an_action()
            self.unit2.perform_an_action()

            if len(self.mapx.bombs) != 0 and pygame.time.get_ticks() - self.mapx.bombs[0][3] > 9500:
                self.mapx.explosion(self.mapx.bombs[0][0], self.mapx.bombs[0][1], self.mapx.bombs[0][2])
                self.mapx.dell_bomb(self.mapx.bombs[0][0], self.mapx.bombs[0][1])
                del self.mapx.bombs[0]
            if len(self.mapx.addBombs) != 0 and pygame.time.get_ticks() - self.mapx.addBombs[0][1] > 1500:
                self.mapx.addBombs[0][0].bomb += 1
                del self.mapx.addBombs[0]
            if len(self.mapx.fire) != 0 and pygame.time.get_ticks() - \
                    self.mapx.fire[0][2] > 200:
                self.mapx.dell_fire(self.mapx.fire[0][0], self.mapx.fire[0][1])
                del self.mapx.fire[0]
            self.mapx.draw_curr_map()
            self.mapx.draw_units()
            for u in units:
                if u.health <= 0:
                    self.run = False
            c1 = f.render("Health of Player1:{}".format(self.unit1.health), True, \
                          [0, 0, 0], [255, 255, 255])
            c2 = f.render("Health of Player2:{}".format(self.unit2.health), True, \
                          [0, 0, 0], [255, 255, 255])
            win.blit(c1, (20, 10))
            win.blit(c2, (20, 24))
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.play()
    pygame.quit()
