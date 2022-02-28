from typing import _SpecialForm
import pygame as pg
import math
from constants import *
pg.font.init()

class Node:
    Node_id = 1
    font = pg.font.SysFont('arial', 15)

    def __init__(self, color, size, coords, src):
        self.color = color
        self.coords = coords
        self.size = size
        self.src = src
        self.hover = False
        self.clicked = False
        self.tangle = []
        self.num = Node.Node_id
        self.offset = pg.font.Font.size(Node.font, str(self.num))
        Node.Node_id += 1
        self.hitbox = pg.draw.circle(self.src, self.color, self.coords, self.size)
        self.src.blit(Node.font.render(str(self.num), True, BLACK), self.coords)


    def render(self, lock):
        if not lock:
            if self.hitbox.collidepoint(pg.mouse.get_pos()) and not self.clicked:
                self.hover = True
                self.color = TEAL
            elif self.clicked:
                self.color = DARKREDDISH
            else:
                self.color = GREY
                self.hover = False
        self.hitbox = pg.draw.circle(self.src, self.color, self.coords, self.size)
        self.src.blit(Node.font.render(str(self.num), True, BLACK), (self.coords[0]-(self.offset[0]//2), self.coords[1]-(self.offset[1]//2)))

class Rib:
    font = pg.font.SysFont('arial', 20)
    def __init__(self, first, second, weight, src):
        self.first = first
        self.second = second
        self.pos_1 = first.coords
        self.pos_2 = second.coords
        self.offset = pg.font.Font.size(Rib.font, str(weight))
        self.weight = weight
        self.src = src
        self.id  = pg.draw.aaline(self.src, BLACK, self.pos_1, self.pos_2, LINE_WIDTH)
        self.text = Rib.font.render(str(self.weight), True, BLACK, WHITE)
        self.hitboxpos = ((self.pos_1[0]+self.pos_2[0])//2 - (self.offset[0]//2), (self.pos_1[1]+self.pos_2[1])//2 - (self.offset[1]//2))
        self.hitbox = self.text.get_rect(topleft = self.hitboxpos)
        self.src.blit(self.text, self.hitboxpos)

    def render(self, texttrig = False):
        self.pos_1 = self.first.coords
        self.pos_2 = self.second.coords
        self.id  = pg.draw.aaline(self.src, BLACK, self.pos_1, self.pos_2, LINE_WIDTH)
        self.text = Rib.font.render(str(self.weight), True, BLACK, WHITE)
        self.hitboxpos = ((self.pos_1[0]+self.pos_2[0])//2 - (self.offset[0]//2), (self.pos_1[1]+self.pos_2[1])//2 - (self.offset[1]//2))
        self.hitbox = self.text.get_rect(topleft = self.hitboxpos)
        if not texttrig:
            self.src.blit(self.text, self.hitboxpos)

    def reweight(self, weight):
        try:
            self.weight = int(weight)
        except:
            if weight.lower() in ('беск','inf','бск','+inf', 'бес'):
                self.weight = float('inf')
            elif weight.lower() in ('-inf', '-бес', '-бск'):
                self.weight = float('-inf')
            else:
                self.weight = SYSWEIGHT
        
        self.offset = pg.font.Font.size(Rib.font, str(weight))


class Graph:
    def __init__(self, src, app) -> None:
        self.model = []
        self.src = src
        self.app = app
        

    def rebuild(self, nodes, lines):
        self.model = [[0 if i == j else 'X' for i in range(len(nodes))] for j in range(len(nodes))]
        for i in lines:
            self.model[i.first.num-1][i.second.num-1] = i.weight


    def dijkstra(self, nodes, lines, start, finish, texttrig):
        weights = [float('inf') for i in range(len(nodes))]
        visited = [False for i in range(len(nodes))]
        weights[start.num-1] = 0
        path = [start]
        
        while path:
            cur = path.pop(0)
            minimal = float('inf')
            # for node in nodes:
            #     if not visited[node.num-1] and weights[node.num-1] <= minimal:
            #         print(f'Новая нода')
            #         dye(node, GREEN, self.src, self.app)
            #         pg.time.delay(DELAY)
            #         minimal = weights[node.num-1]
            #         cur = node
            #         dye(node, GREY, self.src, self.app)
            # if cur == -1:
            #     break
            dye(cur, PURPLE, self.src, self.app)
            stack = []
            for node in nodes:
                if self.model[cur.num-1][node.num-1] != 'X' and node != cur:
                    dye(node, YELLOW, self.src, self.app)
                    pg.time.delay(DELAY)
                    stack.append(node)
                    dye(node, GREY, self.src, self.app)
            path.extend(stack)
            while stack:
                now = stack.pop(0)
                if weights[now.num-1] > weights[cur.num-1] + self.model[cur.num-1][now.num-1]:
                    weights[now.num-1] = weights[cur.num-1] + self.model[cur.num-1][now.num-1]
                    line = [i for i in lines if (cur, now) == (i.first, i.second)]
                    line[0].weight = weights[now.num-1]
                    dye(now, PURPLE, self.src, self.app)
                    pg.time.delay(DELAY)
                    dye(now, GREY, self.src, self.app)
            visited[cur.num-1] = True
            pg.time.delay(DELAY)
        print(weights)


    def dfs(self, nodes, cur, path = []):
        if cur not in path:
            dye(cur, GREEN, self.src, self.app)
            pg.time.delay(DELAY)
            path.append(cur)
            stack = [i for i in nodes if self.model[cur.num-1][i.num-1] != 'X']
            for node in stack:
                path = self.dfs(nodes, node, path)
        # dye(cur, PURPLE, self.src, self.app)
        # pg.time.delay(DELAY)
        return path
        
            

def dye(node, color, src, app, line = None):
    node.color = color
    node.render(True)
    if line:
        line.render()
    src.blit(app, (0,0))
    pg.display.flip()

def rotate(pos, cen, angle):	
    cos_theta = math.cos(angle)
    sin_theta = math.sin(angle)
    ret = ((cos_theta * (pos[0] - cen[0]) - sin_theta * (pos[1] - cen[1])) + cen[0],
    (sin_theta * (pos[0] - cen[0]) + cos_theta * (pos[1] - cen[1])) + cen[1])
    return ret