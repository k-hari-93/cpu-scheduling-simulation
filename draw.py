#!/usr/bin/env python

import sys
import os
import random
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
    color = [0x3EE07A, 0xCCB696, 0xFFFF00, 0x60E3DF, 0xFF0000, 0x7CC4D7, 0x09F4F3, 0x494B97, 0x0000FF, 0xCBBDC5, 0x0BBDDB]

    if not len(sys.argv) == 2:
        raise(Exception("Specify exactly one input file"))
    inFile = sys.argv[1]
    if not os.path.exists(inFile):
        raise(Exception("No such file"))

    f = open(inFile,"r")
    color_map = get_map(f, color)
    color_map["scheduler"] = 0x000000
    f.close()

    f = open(inFile,"r")
    title = f.readline().strip()

    pygame.init()
    BLACK = [0, 0, 0]
    WHITE = [255, 255, 255]
    size = (1366,768)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(title)
    clock = pygame.time.Clock()
    screen.fill(WHITE)
    pygame.display.flip()

    x_cord = 10
    y_cord = 200
    height = 50

    done = False
    flag = 0
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        list = []
        for proc in f:
            if not flag:
                match = re.search("\d+:\w+:\d+",proc)
                if match:
                    list = match.group().split(':')
                    x_offset = int(list[0])
                    p = str(list[1])
                    width = 10*int(list[2])
                    print list, width

                    if x_cord+x_offset >= size[0]:
                        x_cor = 10
                        y_cord += 200
                    else:
                        x_cor = x_cord+x_offset
                screen.fill(color_map[p], [x_cor, y_cord,width,height])

        flag = 1

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
