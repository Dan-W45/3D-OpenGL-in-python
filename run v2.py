import contextlib
with contextlib.redirect_stdout(None):
    import pygame, sys
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

clock = pygame.time.Clock()
width, height = 1280, 720
pygame.init()
pygame.display.set_mode([width, height], DOUBLEBUF|OPENGL)
gluPerspective(75, width/height, 0, 1000)

edges = ((0,1),(0,3),(0,4),(2,1),(2,3),(2,7),(6,3),(6,4),(6,7),(5,1),(5,4),(5,7))
surfaces = ((0,1,2,3),(3,2,7,6),(6,7,5,4),(4,5,1,0),(1,5,7,2),(4,0,3,6))
verticies=((1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 0), (1, 0, 1), (1, 1, 1), (0, 0, 1), (0, 1, 1))
ground_vertices=((-50,-0.1,50),(-50,-0.1,-50),(50,-0.1,-50),(50,-0.1,50),)
sky_surfaces = ((0,1,2,3),(3,2,7,6),(6,7,5,4),(4,5,1,0),(1,5,7,2),(4,0,3,6))

look_up, look_down, look_left, look_right = False, False, False, False
pitch, yaw = 0, 0

grass = (0.21,0.41,0.18)
sky = (0.22, 0.69, 87)

class Cube:
    def __init__(self, position, verticies, interactable = False, colour = (160, 0, 240)):
        self.position = position
        self.verticies = verticies
        self.interactable = interactable
        self.colour = colour
    def wireframe(self):
        glBegin(GL_LINES)
        offset = 0.5
        for edge in edges:
            for vertex in edge:
                glColor3fv(self.colour)
                glVertex3fv((self.position[0] - self.verticies[vertex][0] + offset, self.position[1] - self.verticies[vertex][1] + offset, self.position[2] - self.verticies[vertex][2] + offset))
        glEnd()
    def draw(self):
        glBegin(GL_QUADS)
        offset = 0.5
        for surface in surfaces:
            for vertex in surface:
                glColor3fv(self.colour)
                glVertex3fv((self.position[0] - self.verticies[vertex][0] + offset, self.position[1] - self.verticies[vertex][1] + offset, self.position[2] - self.verticies[vertex][2] + offset))
        glEnd()        

def ground():
    glBegin(GL_QUADS)
    for vertex in ground_vertices:
        glColor3fv(grass)
        glVertex3fv((vertex[0],vertex[1]-0.5,vertex[2]))
    glEnd()

def skybox():
    global verticies
    glBegin(GL_QUADS)
    for surface in sky_surfaces:
        for vertex in surface:
            glColor3fv(sky)
            glVertex3fv((0.5 - verticies[vertex][0], 0.5 - verticies[vertex][1], 0.5 - verticies[vertex][2]))
    glEnd()

def events():
    global look_up, look_down, look_left, look_right
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == K_UP:
                look_up = True
            if event.key == K_DOWN:
                look_down = True
            if event.key == K_LEFT:
                look_left = True
            if event.key == K_RIGHT:
                look_right = True
        if event.type == pygame.KEYUP:
            if event.key == K_UP:
                look_up = False
            if event.key == K_DOWN:
                look_down = False
            if event.key == K_LEFT:
                look_left = False
            if event.key == K_RIGHT:
                look_right = False

def rotate_camera():
    global look_up, look_down, look_left, look_right, pitch, yaw
    if yaw < 0: yaw+=360
    elif yaw >= 360: yaw-=360
    if look_up and pitch > -90:
        pitch -= 2
        glRotate(-yaw,0,1,0)
        glRotate(-2,1,0,0)
        glRotate(yaw,0,1,0)
    if look_down and pitch < 90:
        pitch += 2
        glRotate(-yaw,0,1,0)
        glRotate(2,1,0,0)
        glRotate(yaw,0,1,0)
    if look_left:
        yaw -= 2
        glRotate(-2,0,1,0)
    if look_right:
        yaw += 2
        glRotate(2,0,1,0)
    print(pitch, yaw)

def draw():
    clock.tick(60)
    pygame.display.flip()
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

coords = (0, -1, -2) 
new_cube = Cube(coords, verticies, False, (0,1,1))
another_cube = Cube(coords, verticies)

cube_right = Cube((2,-1,0), verticies, False, (0,0,1))
cube_left = Cube((-2,-1,0), verticies, False, (1,0,0))
cube_behind = Cube((0,-1,2), verticies)

while True:
    events()
    skybox()
    ground()
    new_cube.draw()
    another_cube.wireframe()
    cube_right.draw()
    cube_left.draw()
    cube_behind.draw()
    rotate_camera()
    draw()
