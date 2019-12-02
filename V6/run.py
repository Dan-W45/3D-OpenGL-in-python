import contextlib
with contextlib.redirect_stdout(None):
    import pygame, sys, math, os, math, random
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from ctypes import *

os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
clock = pygame.time.Clock()
pygame.init()
res=pygame.display.list_modes()
width,height=res[0][0],res[0][1]
##width, height = 1280, 720                                                 ####MANUAL RESOLUTION OVERRIDE
width, height = 1024, 576
pygame.display.set_mode([width, height], DOUBLEBUF|OPENGL)
##pygame.display.set_mode([width, height], DOUBLEBUF|OPENGL|FULLSCREEN)
gluPerspective(90, width/height, 0.1,50)

moveforward, movebackward, moveleft, moveright = False, False, False, False
moveup, movedown = False, False
glClearColor(0.5, 0.69, 1.0, 1)

#Mouse/camera rotation stuff
pygame.mouse.set_visible(False)
x,y=0,0
pitch,yaw = 0,0
player_x, player_y, player_z = 0,0,0


def events():
    global pitch, yaw, moveforward, movebackward, moveleft, moveright, moveup, movedown, player_x, player_y, player_Z
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.mouse.set_visible(True)
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                moveforward = True
            if event.key == K_s:
                movebackward = True
            if event.key == K_a:
                moveleft = True
            if event.key == K_d:
                moveright = True
            if event.key == K_SPACE:
                moveup = True
            if event.key == K_LCTRL:
                movedown = True
        if event.type == pygame.KEYUP:
            if event.key == K_w:
                moveforward = False
            if event.key == K_s:
                movebackward = False
            if event.key == K_a:
                moveleft = False
            if event.key == K_d:
                moveright = False
            if event.key == K_SPACE:
                moveup = False
            if event.key == K_LCTRL:
                movedown = False

            if event.key == K_z:
                print(int(clock.get_fps()))
                ##print(player_x, '\n' + str(player_z))

        if event.type == pygame.MOUSEMOTION:
            pygame.mouse.set_pos(width/2,height/2)
            x,y = event.pos
            dx = (x - (width/2))/38
            dy = (y - (height/2))/38
            yaw += dx
            pitch += dy
            glTranslatef(-player_x, -player_y, -player_z)
            glRotatef(dx, 0, 1, 0)                   #Horizontal rotation
            glRotatef(-yaw, 0, 1, 0)
            glRotatef(dy, 1, 0, 0)                   #Vertical rotation
            glRotatef(yaw, 0, 1, 0)

            if pitch > 90:                          #Looking straight down
                glRotatef(-yaw, 0, 1, 0)
                glRotatef(90-pitch, 1, 0, 0)
                glRotatef(yaw, 0, 1, 0)
                pitch = 90
            elif pitch < -90:                       #Looking straight up
                glRotatef(-yaw, 0, 1, 0)
                glRotatef(-90-pitch, 1, 0, 0)
                glRotatef(yaw, 0, 1, 0)
                pitch = -90
            if yaw >= 360: yaw -= 360
            elif yaw <=0 : yaw += 360
            glTranslatef(player_x, player_y, player_z)



def movement():
    global pitch, yaw, moveforward, movebackward, moveleft, moveright, player_x, player_y, player_z
    speed = 0.1
    if moveforward:
        player_x-=math.sin(math.pi*yaw/180)*speed
        player_z+=math.cos(math.pi*yaw/180)*speed
        glTranslatef(-math.sin(math.pi*yaw/180)*speed, 0, 0)
        glTranslatef(0, 0, math.cos(math.pi*yaw/180)*speed)
    if movebackward:
        player_x+=math.sin(math.pi*yaw/180)*speed
        player_z-=math.cos(math.pi*yaw/180)*speed
        glTranslatef(math.sin(math.pi*yaw/180)*speed, 0, 0)
        glTranslatef(0, 0, -math.cos(math.pi*yaw/180)*speed)
    if moveleft:
        player_x+=math.sin(math.pi*(yaw+90)/180)*speed
        player_z-=math.cos(math.pi*(yaw+90)/180)*speed
        glTranslatef(math.sin(math.pi*(yaw+90)/180)*speed, 0, 0)
        glTranslatef(0, 0, -math.cos(math.pi*(yaw+90)/180)*speed)
    if moveright:
        player_x-=math.sin(math.pi*(yaw+90)/180)*speed
        player_z+=math.cos(math.pi*(yaw+90)/180)*speed
        glTranslatef(-math.sin(math.pi*(yaw+90)/180)*speed, 0, 0)
        glTranslatef(0, 0, math.cos(math.pi*(yaw+90)/180)*speed)
    if moveup:
        player_y-=0.1
        glTranslatef(0, -0.1, 0)
    if movedown:
        player_y+=0.1
        glTranslatef(0, 0.1, 0)


glEnableClientState(GL_VERTEX_ARRAY)
##glEnableClientState(GL_COLOR_ARRAY)
glEnableClientState(GL_TEXTURE_COORD_ARRAY)

class Cube:
    def __init__(self,x,y,z):
        self.vertices=[0+x,1+y,0+z, 1+x,1+y,0+z, 1+x,0+y,0+z, 0+x,0+y,0+z,
                       0+x,0+y,0+z, 0+x,0+y,1+z, 0+x,1+y,1+z, 0+x,1+y,0+z,
                       0+x,1+y,0+z, 1+x,1+y,0+z, 1+x,1+y,1+z, 0+x,1+y,1+z,
                       0+x,1+y,1+z, 0+x,0+y,1+z, 1+x,0+y,1+z, 1+x,1+y,1+z,
                       1+x,1+y,1+z, 1+x,1+y,0+z, 1+x,0+y,0+z, 1+x,0+y,1+z,
                       1+x,0+y,1+z, 0+x,0+y,1+z, 0+x,0+y,0+z, 1+x,0+y,0+z]

        self.vbo = glGenBuffers(1, GL_VERTEX_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, len(self.vertices)*4, (c_float*len(self.vertices))(*self.vertices), GL_STATIC_DRAW)

####        self.colorslst=[0.21,0.41,0.18, 0.21,0.41,0.18, 0.34,0.23,0.05, 0.34,0.23,0.05,     #North
####                        0.34,0.23,0.05, 0.34,0.23,0.05, 0.21,0.41,0.18, 0.21,0.41,0.18,     #West
####                        0.21,0.41,0.18, 0.21,0.41,0.18, 0.21,0.41,0.18, 0.21,0.41,0.18,     #Top
####                        0.21,0.41,0.18, 0.34,0.23,0.05, 0.34,0.23,0.05, 0.21,0.41,0.18,     #South
####                        0.21,0.41,0.18, 0.21,0.41,0.18, 0.34,0.23,0.05, 0.34,0.23,0.05,     #East
####                        0.34,0.23,0.05, 0.34,0.23,0.05, 0.34,0.23,0.05, 0.34,0.23,0.05]     #Bottom
##
##        self.colorslst=[0.34,0.23,0.05, 0.34,0.23,0.05, 0.34,0.23,0.05, 0.34,0.23,0.05,     #North
##                        0.34,0.23,0.05, 0.34,0.23,0.05, 0.34,0.23,0.05, 0.34,0.23,0.05,     #West
##                        0.21,0.41,0.18, 0.21,0.41,0.18, 0.21,0.41,0.18, 0.21,0.41,0.18,     #Top
##                        0.34,0.23,0.05, 0.34,0.23,0.05, 0.34,0.23,0.05, 0.34,0.23,0.05,     #South
##                        0.34,0.23,0.05, 0.34,0.23,0.05, 0.34,0.23,0.05, 0.34,0.23,0.05,     #East
##                        0.34,0.23,0.05, 0.34,0.23,0.05, 0.34,0.23,0.05, 0.34,0.23,0.05]     #Bottom
##
##        self.colors = glGenBuffers(1, GL_COLOR_ARRAY)
##        glBindBuffer(GL_ARRAY_BUFFER, self.colors)
##        glBufferData(GL_ARRAY_BUFFER, len(self.colorslst)*4, (c_float*len(self.colorslst))(*self.colorslst), GL_STATIC_DRAW)


    def draw(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glVertexPointer(3,GL_FLOAT,0,None)
##        glBindBuffer(GL_ARRAY_BUFFER, self.colors)
##        glColorPointer(3,GL_FLOAT,0,None)
        glBindTexture(GL_TEXTURE_2D, texid)
        glTexCoordPointer(3,GL_FLOAT,0,None)
##        glDrawArrays(GL_LINES, 0, len(self.vertices))
        glDrawArrays(GL_QUADS, 0, len(self.vertices))




def loadTexture():
    global texid
    textureSurface = pygame.image.load('textures/test_square.png')
    textureData = pygame.image.tostring(textureSurface, "RGB", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()
    glEnable(GL_TEXTURE_2D)

    texid = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texid)
    
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, textureData)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S,GL_REPEAT)
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T,GL_REPEAT)


Cubes=[]
Cubes.append(Cube(0,0,0))
for x in range(-10,10):
    for z in range(-10,10):
        Cubes.append(Cube(x,-2,z))

loadTexture()
while True:
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    events()
    movement()
    for cube in Cubes:
        cube.draw()

    pygame.display.flip()
    clock.tick(60)



