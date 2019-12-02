import contextlib
with contextlib.redirect_stdout(None):
    import pygame, sys, math, os, math, random
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from ctypes import *

#os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
clock = pygame.time.Clock()
pygame.init()
res=pygame.display.list_modes()
width,height=res[0][0],res[0][1]
width, height = 1280, 720                                                 ####MANUAL RESOLUTION OVERRIDE
pygame.display.set_mode([width, height], DOUBLEBUF|OPENGL)
gluPerspective(70, width/height, 0.1,50)

def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.mouse.set_visible(True)
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_w:
                glTranslate(0,0,1)
            if event.key == K_s:
                glTranslate(0,0,-1)
            if event.key == K_a:
                glTranslate(1,0,0)
            if event.key == K_d:
                glTranslate(-1,0,0)
            if event.key == K_q:
                glTranslate(0,-1,0)
            if event.key == K_e:
                glTranslate(0,1,0)

            if event.key == K_LEFT:
                glRotate(-4,0,1,0)
            if event.key == K_RIGHT:
                glRotate(4,0,1,0)



glEnableClientState(GL_VERTEX_ARRAY)


vertices=[-1,1,-1, 1,1,-1, 1,-1,-1, -1,-1,-1,    -1,-1,-1, -1,-1,1, -1,1,1, -1,1,-1,    -1,1,-1, 1,1,-1, 1,1,1, -1,1,1,    -1,1,1, -1,-1,1, 1,-1,1, 1,1,1,    1,1,1, 1,1,-1, 1,-1,-1, 1,-1,1,    1,-1,1, -1,-1,1, -1,-1,-1, 1,-1,-1]

vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, len(vertices)*4, (c_float*len(vertices))(*vertices), GL_STATIC_DRAW)

def vbo_cube():
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glVertexPointer(3,GL_FLOAT,0,None)
    #glDrawArrays(GL_LINES, 0, len(vertices))
    glDrawArrays(GL_QUADS, 0, len(vertices))

glTranslate(0,0,-3)
while True:
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    events()
    #glRotate(-1,1,1,0)
    vbo_cube()

    pygame.display.flip()
    clock.tick(60)



