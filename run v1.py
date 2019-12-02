import pygame, sys, math, random, os
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

clock = pygame.time.Clock()
pygame.init()
width, height = 1280, 720
g=pygame.display.set_mode([width, height], DOUBLEBUF|OPENGLBLIT)
gluPerspective(90, width/height, 0.1, 1000.0)
font=pygame.font.SysFont("Sans MS", 60)

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )

def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()            

def Cube():
    glBegin(GL_LINES)
    cube = [(0, 0, -2), ((1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 0), (1, 0, 1), (1, 1, 1), (0, 0, 1), (0, 1, 1)), (0, 0, 55)]
    cube_location = cube[0]
    Lverticies=cube[1]
    off_val=0.5
    for edge in edges:
        for vertex in edge:
            x=cube_location[0]-Lverticies[vertex][0]+off_val
            y=cube_location[1]-Lverticies[vertex][1]+off_val
            z=cube_location[2]-Lverticies[vertex][2]+off_val
            glColor3fv((255,0,0))
            glVertex3fv((x,y,z))
    glEnd()

def FilledCube():
    glBegin(GL_QUADS)
    cube = [(1.2, -0.6, -2), ((1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 0), (1, 0, 1), (1, 1, 1), (0, 0, 1), (0, 1, 1)), (0, 0, 55)]
    cube_location = cube[0]
    Lverticies=cube[1]
    off_val=0.5
    for surface in surfaces:
        for vertex in surface:
            x=cube_location[0]-Lverticies[vertex][0]+off_val
            y=cube_location[1]-Lverticies[vertex][1]+off_val
            z=cube_location[2]-Lverticies[vertex][2]+off_val
            glColor3fv((0,155,155))
            glVertex3fv((x,y,z))
    glEnd()


def draw():
    clock.tick(60)
    text = font.render('Hello', True, pygame.Color('red'))
    g.blit(text,(50,50))
    pygame.display.flip()

while True:
    events()
    FilledCube()
    Cube()
    draw()
