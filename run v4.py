import contextlib
with contextlib.redirect_stdout(None):
    import pygame, sys, math, os, math, random
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
##pygame.display.set_mode([width, height], DOUBLEBUF|OPENGL|FULLSCREEN)
gluPerspective(70, width/height, 0.1,50)
pygame.mouse.set_visible(False)
#print(pygame.font.get_fonts())
font = pygame.font.Font (None, 40)

sin = math.sin
cos = math.cos

vertices = ((1, -1, -1),(1, 1, -1),(-1, 1, -1),(-1, -1, -1),(1, -1, 1),(1, 1, 1),(-1, -1, 1),(-1, 1, 1))       #Big cubes

edges = ((0,1),(0,3),(0,4),(2,1),(2,3),(2,7),(6,3),(6,4),(6,7),(5,1),(5,4),(5,7))
surfaces = ((0,1,2,3),(3,2,7,6),(6,7,5,4),(4,5,1,0),(1,5,7,2),(4,0,3,6))
vertices=((1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 0), (1, 0, 1), (1, 1, 1), (0, 0, 1), (0, 1, 1))
ground_vertices =((1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 0), (1, 0, 1), (1, 1, 1), (0, 0, 1), (0, 1, 1))

#Colours:
grass = (0.21,0.41,0.18)
sky = (0.22, 0.69, 87)

#Mouse/camera rotation stuff
x,y=0,0
pitch,yaw = 0,0

#Player rotation stuff
player_x, player_y, player_z = 0,1,0
y_force = 0
acceleration = 0.01
lasty = 0
current_ground = 0


moveforward, movebackward, moveleft, moveright, moveup, movedown, run = False, False, False, False, False, False, False
look_up, look_down, look_left, look_right = False, False, False, False

def events():
    global pitch, yaw, moveforward, movebackward, moveleft, moveright, moveup, movedown, run
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.mouse.set_visible(True)
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.mouse.set_pos(width/2,height/2)
            x,y = event.pos
            dx = (x - (width/2))/38
            dy = (y - (height/2))/38
            yaw += dx
            pitch += dy
            glRotate(dx, 0, 1, 0)                   #Horizontal rotation
            glRotate(-yaw, 0, 1, 0)
            glRotate(dy, 1, 0, 0)                   #Vertical rotation
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


        global look_up, look_down, look_left, look_right
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
            if event.key == K_LSHIFT:
                run = True
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
            if event.key == K_LSHIFT:
                run = False

def movement():
    global pitch, yaw, player_x, player_y, player_z, moveforward, movebackward, moveleft, moveright, moveup, movedown, run, y_force, acceleration, lasty, current_ground, collide
    speed = 0.1
    forward_speed = 0.1
    if run:
        forward_speed = 0.2
        speed = 0.1
    if moveforward:
        player_x += sin(math.pi*yaw/180)*forward_speed
        player_z -= cos(math.pi*yaw/180)*forward_speed
    if movebackward:
        player_x -= sin(math.pi*yaw/180)*speed
        player_z += cos(math.pi*yaw/180)*speed
    if moveleft:
        player_x -= sin(math.pi*(yaw+90)/180)*speed
        player_z += cos(math.pi*(yaw+90)/180)*speed
    if moveright:
        player_x -= sin(math.pi*(yaw-90)/180)*speed
        player_z += cos(math.pi*(yaw-90)/180)*speed
    if moveup and collide:
        acceleration = 0.15
##    if movedown and player_y < 0:
##        player_y += 0.1

    global look_up, look_down, look_left, look_right
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


    lasty = player_y
    if not collide or acceleration != 0:
        player_y += acceleration
        if player_y <= current_ground:
            player_y = current_ground
            #acceleration -= 1
            if lasty == player_y:
                acceleration = 0
        acceleration -= 0.01
        #print(player_y)


class Cube:
    def __init__(self, position, vertices, interactable = False, colour = (160, 0, 240)):
        self.position = position
        self.vertices = vertices
        self.interactable = interactable
        self.colour = colour
    def wireframe(self):
        glBegin(GL_LINES)
        offset = 0.5
        for edge in edges:
            for vertex in edge:
                glColor3fv(self.colour)
                glVertex3fv((self.position[0] - self.vertices[vertex][0] + offset - player_x, self.position[1] - self.vertices[vertex][1] + offset - player_y, self.position[2] - self.vertices[vertex][2] + offset - player_z))
        glEnd()
    def draw(self):
        glBegin(GL_QUADS)
        offset = 0.5
        for surface in surfaces:
            for vertex in surface:
                glColor3fv(self.colour)
                glVertex3fv((self.position[0] - self.vertices[vertex][0] + offset - player_x, self.position[1] - self.vertices[vertex][1] + offset - player_y, self.position[2] - self.vertices[vertex][2] + offset - player_z))
        glEnd()

def skybox():
    global vertices
    glBegin(GL_QUADS)
    for surface in surfaces:
        for vertex in surface:
            glColor3fv(sky)
            glVertex3fv((0.5 - vertices[vertex][0], 0.5 - vertices[vertex][1], 0.5 - vertices[vertex][2]))
    glEnd()

def sun():
    global vertices
    position = (0,6,0)
    colour = (1,0.9,0.3)
    glBegin(GL_QUADS)
    offset = 0.5
    for surface in surfaces:
        for vertex in surface:
            glColor3fv(colour)
            glVertex3fv((position[0] - vertices[vertex][0] + offset, position[1] - vertices[vertex][1] + offset, position[2] - vertices[vertex][2] + offset))
    glEnd()        

def drawText(position, textString, textcolour):
    glEnable( GL_ALPHA_TEST )
    glAlphaFunc( GL_GREATER, 0.5 )
    textSurface = font.render(textString, True, textcolour)
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glRasterPos2i(*position)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

def crosshair():
    glLineWidth(3)
    glBegin(GL_LINES)
    glColor3fv((0,0,0))
    glVertex2f(width/2-15,height/2)
    glVertex2f(width/2+15,height/2)
    glVertex2f(width/2,height/2-15)
    glVertex2f(width/2,height/2+15)
    glEnd()

cube_list=[]
def gen_cubes():
    global cube_list, vertices
    for x in range(-2,2):
        for z in range(-2,2):
            coords = (x, -1, z)
            cube_list.append(Cube(coords, vertices, False, grass))
##    cube_list.append(Cube((0,0,-1), ground_vertices, False, grass))

def draw_cubes():
    global cube_list
    for cube in cube_list:
        cube.draw()

def alt_draw():
    global cube_list
    offset = 0.5
    glBegin(GL_QUADS)
    for cube in cube_list:
        for surface in surfaces:
            for vertex in surface:
                glColor3fv(cube.colour)
                glVertex3fv((cube.position[0] - cube.vertices[vertex][0] + offset - player_x, cube.position[1] - cube.vertices[vertex][1] + offset - player_y, cube.position[2] - cube.vertices[vertex][2] + offset - player_z))
    glEnd()


def collision():                                                ##Not yet working
    global cube_list, player_x, player_y, player_z, collide, acceleration, current_ground
    collide = False
    current_ground = 0
    for cube in cube_list:
##        print(cube.position)
        cube_pos = cube.position
        cube_pos_x = cube_pos[0]
        cube_pos_y = cube_pos[1]
        cube_pos_z = cube_pos[2]


        #print(cube_pos_x-1,cube_pos_x+1)


        #if (int(player_x) in range(cube_pos_x-1,cube_pos_x+1)) and (int(player_z) in range(cube_pos_z-1,cube_pos_z+1)):
        #    collide = True
        #else: collide = False

        if cube_pos_x-1<player_x<cube_pos_x+1 and cube_pos_y-1<player_y-1<cube_pos_y+1 and cube_pos_z-1<player_z<cube_pos_z+1:
            collide = True
            if player_y-1<cube_pos_y+1:
                #print('you in a cube')
                current_ground = cube_pos_y+2
                #player_y = cube_pos_y+2
                acceleration = 0


coords = (0, 0, -2)
new_cube = Cube(coords, vertices, False, (0,1,1))
##new_cube_pt2 = Cube(coords, vertices)

cube_right = Cube((2,0,0), vertices, False, (0,1,0))
cube_left = Cube((-2,0,0), vertices, False, (1,0,0))
cube_behind = Cube((0,0,2), vertices)

##print(new_cube.position)
gen_cubes()
collide = False
glClearColor(0.5, 0.69, 1.0, 1)
#glClearColor(0.22, 0.69, 87,1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_CULL_FACE)
while True:
    pygame.mouse.set_visible(False)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    events()
    movement()
##    glDisable(GL_DEPTH_TEST)
##    skybox()
##    glEnable(GL_DEPTH_TEST)
    sun()
##    draw_cubes()
    alt_draw()
##    new_cube.draw()
####    new_cube_pt2.wireframe()
##    cube_right.draw()
##    cube_left.draw()
##    cube_behind.draw()
    collision()

    ##Change to render 2D
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, width, height, 0)

##    glDisable(GL_DEPTH_TEST)
##    glDisable(GL_CULL_FACE)
##    glDisable(GL_TEXTURE_2D)
##    glDisable(GL_LIGHTING)

    glClear(GL_DEPTH_BUFFER_BIT)

    ##ANY 2D CODE GOES HERE
    if int(clock.get_fps()) >=60:
        fpscolour = (0,255,0)
    elif 30 < int(clock.get_fps()) < 60:
        fpscolour = (255,255,0)
    elif int(clock.get_fps()) < 30:
        fpscolour = (255,0,0)
    drawText((0,27),str(int(clock.get_fps()))+" FPS", fpscolour)

    crosshair()

    if collide:
        drawText((640,360),str("Collision"), (255,255,255))
        
    
    ##Revert back to 3D
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

    pygame.display.flip()
    clock.tick(60)

    
