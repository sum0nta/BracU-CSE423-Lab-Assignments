'''Task 1'''
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

rain_drops = [(random.randint(0, 500), random.randint(0, 500)) for i in range(100)]
direction = 0
background_color = 0
rain_speed = 2


def draw_square(x, y):
    glLineWidth(4.0)
    glBegin(GL_LINES)
    glVertex2f(x, y)
    glVertex2f(x + 200, y)
    glVertex2f(x, y + 150)
    glVertex2f(x + 200, y + 150)
    glVertex2f(x, y)
    glVertex2f(x, y + 150)
    glVertex2f(x + 200, y)
    glVertex2f(x + 200, y + 150)
    glEnd()

def draw_triangle(x, y):
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y + 150)
    glVertex2f(x + 200, y + 150)
    glVertex2f(x + 100, y + 200)
    glEnd()

def draw_door(x, y):
    glBegin(GL_LINES)
    glVertex2f(x + 50, y)
    glVertex2f(x + 50, y + 50)
    glVertex2f(x + 50, y + 50)
    glVertex2f(x + 75, y + 50)
    glVertex2f(x + 75, y + 50)
    glVertex2f(x + 75, y)
    glEnd()

def draw_doorknob(x, y):
    glPointSize(5)
    glBegin(GL_POINTS)
    glVertex2f(x + 65, y + 25)
    glEnd()

def draw_window(x, y):
    glLineWidth(1.0)
    glBegin(GL_LINES)
    glVertex2f(x + 120, y + 80)
    glVertex2f(x + 170, y + 80)
    glVertex2f(x + 120, y + 80)
    glVertex2f(x + 120, y + 110)
    glVertex2f(x + 120, y + 110)
    glVertex2f(x + 170, y + 110)
    glVertex2f(x + 170, y + 110)
    glVertex2f(x + 170, y + 80)
    glVertex2f(x + 145, y + 80)
    glVertex2f(x + 145, y + 110)
    glVertex2f(x + 120, y + 95)
    glVertex2f(x + 170, y + 95)
    glEnd()


def update_rain():
    global rain_drops
    for i in range(len(rain_drops)):
        rain_drops[i] = (rain_drops[i][0] + direction * 5, rain_drops[i][1] - rain_speed)
        if rain_drops[i][1] < 0:
            rain_drops[i] = (random.randint(0, 500), 500)

def draw_rain():
    glBegin(GL_LINES)
    for x, y in rain_drops:
        glVertex2f(x, y)
        glVertex2f(x, y-10)
    glEnd()

def changeDay():
    global background_color
    background_color = min(0.7, background_color + 0.05)

def changeNight():
    global background_color
    background_color = max(0.0, background_color - 0.05)

def rainLeftShift():
    global direction
    direction = max(-0.5, direction - 0.02)

def rainRightShift():
    global direction
    direction = min(0.5, direction + 0.02)

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def display():
    global background_color
    glClearColor(background_color, background_color, background_color, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 1.0, 1.0)
    draw_rain()
    draw_square(150, 150)
    draw_triangle(150, 150)
    draw_door(150, 150)
    draw_doorknob(150, 150)
    draw_window(150, 150)
    
    glutSwapBuffers()

def keyboardListener(key,x,y):
    if key == b'a':  
        changeDay()
    elif key == b'd':  
        changeNight()

def specialKeyListener(key,x,y):
    if key == GLUT_KEY_LEFT:
        rainLeftShift()
    elif key == GLUT_KEY_RIGHT:
        rainRightShift()


def animate():
    update_rain()
    glutPostRedisplay()


glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"House Rain")
glutDisplayFunc(display)
glutIdleFunc(animate) 
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMainLoop()




'''Task 2'''
# from OpenGL.GL import *
# from OpenGL.GLUT import *
# from OpenGL.GLU import *
# import random
# import time


# points = []  
# speed = 1
# blinking = False  
# blinkSt = None
# frozen = False  

# width = 500
# height = 500

# def update_points():
#     global points, blinking, blinkSt, frozen

#     if frozen:
#         return 

#     if blinking:
#         current_time = time.time()
#         elapsed_time = current_time - blinkSt
#         blinkSt = int(elapsed_time*5) % 2 
#         points = [(x, y, dx, dy, bool(blinkSt)) for x, y, dx, dy, i in points]

#     for i in range(len(points)):
#         x, y, dx, dy, blinkSt = points[i]
#         x += dx * speed
#         y += dy * speed

#         if x >= width / 2 or x <= -width / 2:
#             dx = -dx
#         if y >= height / 2 or y <= -height / 2:
#             dy = -dy

#         points[i] = (x, y, dx, dy, blinkSt)

    

# def keyboardListener(key, x, y):
#     global frozen
#     if key == b' ':
#         frozen = not frozen
    
# def specialKeyListener(key, x, y):
#     global points, frozen

#     if frozen:
#         return 

#     if key == GLUT_KEY_UP:  
#         points = [(x, y, dx * 1.1, dy * 1.1, blinkSt) for x, y, dx, dy, blinkSt in points]
#     elif key == GLUT_KEY_DOWN: 
#         points = [(x, y, dx * 0.9, dy * 0.9, blinkSt) for x, y, dx, dy, blinkSt in points]

# def mouseListener(button, state, x, y): 
#     global blinking, blinkSt, frozen

#     if frozen:
#         return 


#     if button == GLUT_LEFT_BUTTON:
#         if state == GLUT_DOWN:
#             blinking = not blinking
#             if blinking:
#                 blinkSt = time.time()
    
#     elif button == GLUT_RIGHT_BUTTON:
#         if state == GLUT_DOWN:
       
#             opengl_x = x - width / 2
#             opengl_y = -(y - height / 2)
#             dx = random.randint(-3.0, 3.0)
#             dy = random.randint(-3.0, 3.0)
#             points.append((opengl_x, opengl_y, dx, dy, True)) 

# def display():
#     glClear(GL_COLOR_BUFFER_BIT)
#     glPointSize(5)
    
#     glBegin(GL_POINTS)
#     for x, y, _, _, blinkSt in points:
#         if not blinking or blinkSt:
#             glColor3f(random.choice([0,1]),random.choice([0,1]),random.choice([0,1]))
#         else:
#             glColor3f(0.0, 0.0, 0.0) 
#         glVertex2f(x, y)
#     glEnd()

#     glutSwapBuffers()

# def animate():
#     update_points()
#     glutPostRedisplay()

# def init():
#     glClearColor(0,0,0,0)
#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     glOrtho(-width / 2, width / 2, -height / 2, height / 2, -1, 1)
   

# glutInit()

# glutInitWindowSize(width, height)
# glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
# glutInitWindowPosition(0, 0)
# glutCreateWindow(b"Amazing Box")

# init()

# glutDisplayFunc(display)
# glutIdleFunc(animate)
# glutMouseFunc(mouseListener)
# glutKeyboardFunc(keyboardListener)
# glutSpecialFunc(specialKeyListener)

# glutMainLoop()