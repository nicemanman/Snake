import math
import random

import pygame
import tkinter as tk
from tkinter import messagebox

borderBam = False;
class Cube(object):
    rows = 40
    w = 600

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        distance = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*distance+1, j*distance+1, distance - 2, distance - 2))



class Snake(object):

    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirnx = 1
        self.dirny = 0

    def move(self):
        global borderBam
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT] and self.dirnx != 1:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_RIGHT] and self.dirnx != -1:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_UP] and self.dirny != 1:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_DOWN] and self.dirny != -1:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    borderBam = True
                    return
                elif c.dirnx == 1 and c.pos[0] >= rows - 1:
                    borderBam = True
                    return
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    borderBam = True
                    return
                elif c.dirny == -1 and c.pos[1] <= 0:
                    borderBam = True
                    return
                else:
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 1;
        self.dirny = 0;

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy


    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    sizeBetween = w // rows  # деление с округлением
    x = 0
    y = 0
    for l in range(rows):
        x += sizeBetween
        y += sizeBetween

        pygame.draw.line(surface, (128, 128, 128), (x, 0), (x, w))
        pygame.draw.line(surface, (128, 128, 128), (0, y), (w, y))


def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()


def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x,y), positions ))) > 0:
            continue
        else:
            break
    return x, y


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global rows, width, s, flag, snack, borderBam
    width = 600
    rows = 40
    win = pygame.display.set_mode((width, width))
    pygame.display.set_caption("Змейка")
    s = Snake((255, 0, 0), (10, 10))
    snack = Cube(randomSnack(rows, s), color=(0, 255, 0))
    flag = True
    clock = pygame.time.Clock()
    while flag:
        pygame.time.delay(50)  # lower value - game faster
        clock.tick(10)  # lower value - game slower
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = Cube(randomSnack(rows, s), color=(0, 255, 0))

        for x in range(len(s.body)):
            if borderBam or s.body[x].pos in list(map(lambda z:z.pos, s.body[x + 1:])):
                message_box("You lost!", "Play again")
                borderBam = False
                s.reset((10, 10))
                break
        redrawWindow(win)



main()



