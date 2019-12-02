import contextlib
with contextlib.redirect_stdout(None):
    import pygame, sys, math, os, ctypes
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
clock = pygame.time.Clock()
pygame.init()
res=pygame.display.list_modes()
width,height=res[0][0],res[0][1]
width, height = 1280, 720                                                 ####MANUAL RESOLUTION OVERRIDE
pygame.display.set_mode([width, height], DOUBLEBUF|OPENGL)
gluPerspective(70, width/height, 0, 1000)
pygame.mouse.set_visible(False)


verticies = ((1, -1, -1),(1, 1, -1),(-1, 1, -1),(-1, -1, -1),(1, -1, 1),(1, 1, 1),(-1, -1, 1),(-1, 1, 1))   #Idk

edges = ((0,1),(0,3),(0,4),(2,1),(2,3),(2,7),(6,3),(6,4),(6,7),(5,1),(5,4),(5,7))
surfaces = ((0,1,2,3),(3,2,7,6),(6,7,5,4),(4,5,1,0),(1,5,7,2),(4,0,3,6))
verticies=((1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 0), (1, 0, 1), (1, 1, 1), (0, 0, 1), (0, 1, 1))
ground_vertices=((-50,-0.1,50),(-50,-0.1,-50),(50,-0.1,-50),(50,-0.1,50))

#Colours:
grass = (0.21,0.41,0.18)
sky = (0.22, 0.69, 87)

#Mouse/camera rotation stuff
x,y=0,0
pitch,yaw = 0,0

def ground():
    glBegin(GL_QUADS)
    for vertex in ground_vertices:
        glColor3fv((0,155,0))
        glVertex3fv((vertex[0],vertex[1]-0.5,vertex[2]))
    glEnd()


def events():
    global pitch, yaw
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.mouse.set_visible(True)
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.mouse.set_pos(width/2,height/2)
            x,y = event.pos
            dx = (x - (width/2))/18
            dy = (y - (height/2))/18
            yaw += dx
            pitch += dy
            glRotate(dx, 0, 1, 0)
            glRotate(-yaw, 0, 1, 0)
            glRotate(dy, 1, 0, 0)
            glRotate(yaw, 0, 1, 0)

            if pitch > 90:                          #Looking straight down
                glRotate(-yaw, 0, 1, 0)
                glRotate(90-pitch, 1, 0, 0)
                glRotate(yaw, 0, 1, 0)
                pitch = 90
            elif pitch < -90:                       #Looking straight up
                glRotate(-yaw, 0, 1, 0)
                glRotate(-90-pitch, 1, 0, 0)
                glRotate(yaw, 0, 1, 0)
                pitch = -90
            if yaw >= 360: yaw -= 360
            elif yaw <=0 : yaw += 360

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
    for surface in surfaces:
        for vertex in surface:
            glColor3fv(sky)
            glVertex3fv((0.5 - verticies[vertex][0], 0.5 - verticies[vertex][1], 0.5 - verticies[vertex][2]))
    glEnd()

coords = (0, -1, -2) 
new_cube = Cube(coords, verticies, False, (0,1,1))
new_cube_pt2 = Cube(coords, verticies)

cube_right = Cube((2,-1,0), verticies, False, (0,0,1))
cube_left = Cube((-2,-1,0), verticies, False, (1,0,0))
cube_behind = Cube((0,-1,2), verticies)
sun = Cube((0,6,0),verticies, False, (1,0.9,0.3))

while True:
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    events()
    skybox()
    ground()
    new_cube.draw()
    new_cube_pt2.wireframe()
    cube_right.draw()
    cube_left.draw()
    cube_behind.draw()
    sun.draw()
    pygame.display.flip()
    clock.tick(60)
    
