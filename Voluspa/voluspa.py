from tkinter import N
import sys
import os

try:
    import pygame as pg
except:
    os.system('pip install pygame')
    os.execv(sys.executable, ['python'] + sys.argv)
try:
    from pygame_textinput import TextInputVisualizer, TextInputManager
except:
    os.system('pip install pygame_textinput')
    os.execv(sys.executable, ['python'] + sys.argv)
from pygame.locals import *
from constants import *
from objects import Node, Rib, Graph




def main():
    pg.init()
    if pg.display.get_init:
        sc = pg.display.set_mode((WIDTH, HEIGHT))
        app = pg.Surface((WIDTH, HEIGHT))
    pg.display.set_caption('Система "Волуспа"')
    icon = pg.image.load(os.path.join(os.getcwd(), 'assets', 'icon.png'))
    pg.display.set_icon(icon)
    graph = Graph(sc, app)
    clock = pg.time.Clock()
    manager = TextInputManager(validator=lambda input: len(input) <= 14)
    text = TextInputVisualizer(manager = manager, font_object = Rib.font)
    ar = []
    linear = []
    cnt = 0
    buf = None
    drag = None
    dragtrig = False
    texttrig = False
    curtext = None
    while 1:
        events = pg.event.get()

        for event in events:
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_RETURN:
                curtext.reweight(text.value)
                graph.rebuild(ar, linear)
                texttrig = False
                

            if not texttrig:
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if not any(node.hitbox.collidepoint(event.pos) for node in ar):
                        ar.append(Node(GREY, NODE_SIZE, event.pos, app))
                        graph.rebuild(ar, linear)
                    
                    else:
                        dragtrig = True
                        for node in ar:
                            if node.hitbox.collidepoint(event.pos):
                                if cnt == 1:
                                    if [buf, node] not in linear and buf != node:
                                        linear.append(Rib(buf, node, SYSWEIGHT, app))
                                        graph.rebuild(ar, linear)
                                    buf.clicked = False
                                    buf = None
                                    cnt = 0
                                else:
                                    buf = node
                                    buf.clicked = True
                                    cnt = 1

                elif event.type == MOUSEBUTTONDOWN and event.button == 3:
                    for i in linear:
                        if i.hitbox.collidepoint(event.pos):
                            texttrig = True
                            curtext = i

                elif event.type == MOUSEMOTION:
                    for node in ar:
                        if node.clicked and dragtrig:
                            drag = node
                            drag.coords = event.pos
                
                elif event.type == MOUSEBUTTONUP and event.button == 1:
                    dragtrig = False
                    if drag:
                        drag.clicked = False
                        drag = None
                        buf = None
                        cnt = 0

                elif event.type == KEYDOWN:
                    if event.key == K_l and ar:
                        graph.dijkstra(ar, linear, ar[0], ar[-1], texttrig)

                    elif event.key == K_j and ar:
                        out = graph.dfs(ar, ar[0], path = [])
                        out = list(reversed(list(map(lambda x: x.num, out))))
                        print(out)

                    
                keys = pg.key.get_pressed()
                if keys[K_x] and keys[K_LSHIFT]:
                    Node.Node_id = 1
                    del ar
                    del linear
                    ar = []
                    linear = []
                    graph.rebuild(ar, linear)

                for node in range(len(ar)):
                    if keys[K_x] and ar[node].clicked:
                        linear = list([i for i in linear if ar[node] not in (i.first, i.second)])
                        del ar[node]
                        for i in range(node, len(ar)):
                            ar[i].num -= 1
                        Node.Node_id -= 1
                        buf = None
                        cnt = 0
                        graph.rebuild(ar, linear)
                        break


        app.fill(WHITE)
        if texttrig:
            text.update(events)
            surf = pg.Surface(text.surface.get_size())
            surf.fill(WHITE)
            app.blit(surf, curtext.hitboxpos)
            app.blit(text.surface, curtext.hitboxpos)


        for i in linear:
            i.render(texttrig)
        for i in ar:
            i.render(False)
        sc.blit(app, (0,0))
        pg.display.flip()
        clock.tick(FPS)
                
            
if __name__ == '__main__':
    main()
