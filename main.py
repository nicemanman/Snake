import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
from Cube import Cube
from Snake import Snake
import WindowSettings
import GameProcessFlags

def drawGrid(surface):
    sizeBetween = WindowSettings.FieldSize // WindowSettings.FieldRows  # деление с округлением
    x = 0
    y = 0
    for l in range(WindowSettings.FieldRows):
        x += sizeBetween
        y += sizeBetween

        pygame.draw.line(surface, (128, 128, 128), (x, 0), (x, WindowSettings.FieldSize))
        pygame.draw.line(surface, (128, 128, 128), (0, y), (WindowSettings.FieldSize, y))


def redrawWindow(surface):
    global s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(surface)
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
    global s, flag, snack, CollisionFlag

    win = pygame.display.set_mode((WindowSettings.FieldSize, WindowSettings.FieldSize))
    pygame.display.set_caption("Змейка")
    s = Snake((255, 0, 0), (10, 10))
    snack = Cube(randomSnack(WindowSettings.FieldRows, s), color=(0, 255, 0))
    flag = True
    clock = pygame.time.Clock()
    while flag:
        pygame.time.delay(50)  # lower value - game faster
        clock.tick(10)  # lower value - game slower
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = Cube(randomSnack(WindowSettings.FieldRows, s), color=(0, 255, 0))

        for x in range(len(s.body)):
            if GameProcessFlags.CollisionFlag or s.body[x].pos in list(map(lambda z:z.pos, s.body[x + 1:])):
                message_box("You lost!", "Play again")
                GameProcessFlags.CollisionFlag = False
                s.reset((10, 10))
                break
        redrawWindow(win)


main()



