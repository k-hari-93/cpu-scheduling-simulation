#!/usr/bin/env python

import sys
import os
import re
import pygame

def get_map(f, color):
    map = {}
    j = 0
    for line in f:
        match = re.search("\d+:\w+",line)
        if match:
            if not match.group().split(':')[1] in map:
                map[match.group().split(':')[1]] = color[j]
                j += 1
    return map

def main():
    color = [0x9C09C8, 0x3EE07A, 0xCCB696, 0xFFFF00, 0x60E3DF, 0x0000FF, 0xFF000, 0x85294B, 0x280409, 0xA21EBD, 0x09F4F3, 0x494B97, 0xCBBDC5, 0x0BBDDB]

    if not len(sys.argv) == 2:
        raise(Exception("Specify exactly one input file"))
    inFile = sys.argv[1]
    if not os.path.exists(inFile):
        raise(Exception("No such file"))

    f = open(inFile,"r")
    color_map = get_map(f, color)
    color_map["scheduler"] = 0xD8680E
    f.close()

    f = open(inFile,"r")
    title = f.readline().strip()

    pygame.init()

    BLACK = [0, 0, 0]
    WHITE = [255, 255, 255]
    size = (1366,768)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Gantt Chart")
    clock = pygame.time.Clock()
    screen.fill(WHITE)

    _font = pygame.font.SysFont('Times New Roman', 30, True, False)
    text = _font.render(title, True, BLACK)
    screen.blit(text, [50,100])

    x_cord = 10
    y_cord = 200
    height = 50
    x_cor = 0
    flag = 1
    list = []
    for proc in f:
        match = re.search("\d+:\w+:\d+",proc)
        match2 = re.search("Avera\w+.+",proc)
        if match:
            list = match.group().split(':')
            time = int(list[0])
            p = str(list[1])
            width = 8*int(list[2])

            if x_cord+width+x_cor >= size[0]-10:
                x_cord = 10
                y_cord += 100
                x_cor = 0
            else:
                x_cord += x_cor
            screen.fill(color_map[p], [x_cord, y_cord, width, height])
            pygame.draw.rect(screen, BLACK, [x_cord, y_cord, width, height], 4)
            font = pygame.font.SysFont('Times New Roman', 18, True, False)
            if not p == 'scheduler':
                text = font.render(p, True, BLACK)
                screen.blit(text, [x_cord+5,y_cord+5])
            text = font.render(str(time), True, BLACK)
            screen.blit(text, [x_cord,y_cord-20])
            x_cor = width
        elif match2:
            string = match2.group().strip()
            text = _font.render(string, True, BLACK)
            if flag:
                screen.blit(text, [50,400])
                flag = 0
            else:
                screen.blit(text, [50,450])

    text = font.render(str(time+x_cor/8), True, BLACK)
    screen.blit(text, [x_cord+x_cor-20,y_cord-20])



    pygame.display.flip()
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

    clock.tick(60)

    pygame.quit()
    f.close()

if __name__ == "__main__":
    main()
