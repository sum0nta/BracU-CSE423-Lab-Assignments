from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random


screenWidth = 500
screenHeight = 500
ship_x = 200
ship_y = 0
projectliles = []
falling_circles = []
falling_circles_speed = 1
score = 0
missed_circles = 0
gameOver = False
paused = False
circle_radius = 10
ship_height, ship_width = 150, 150
buttonWidth,buttonHeight = 100,50
restart_button_x, restart_button_y = 10, screenHeight - buttonHeight
play_pause_button_x, play_pause_button_y = 120, screenHeight - buttonHeight
terminate_button_x, terminate_button_y = 230, screenHeight - buttonHeight


def setPixel(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def findZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) > abs(dy):
        if dx > 0 and dy >= 0:
            return 0
        elif dx <= 0 and dy > 0:
            return 3
        elif dx < 0 and dy <= 0:
            return 4
        else:
            return 7
    else:
        if dx >= 0 and dy > 0:
            return 1
        elif dx < 0 and dy >= 0:
            return 2
        elif dx <= 0 and dy < 0:
            return 5
        else:
            return 6

def ConvertMtoZero(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y

def ConvertZeroToM(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y

def midpointLine(x1, y1, x2, y2, zone):
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)
    x, y = x1, y1

    cx, cy = ConvertMtoZero(x, y, zone)
    setPixel(cx, cy)

    while x < x2:
        if d <= 0:
            d += incE
            x += 1
        else:
            d += incNE
            x += 1
            y += 1

        cx, cy = ConvertZeroToM(x, y, zone)
        setPixel(cx, cy)

def midpointLineEightWay(x1, y1, x2, y2):
    zone = findZone(x1, y1, x2, y2)
    ax1, ay1 = ConvertMtoZero(x1, y1, zone)
    ax2, ay2 = ConvertMtoZero(x2, y2, zone)
    midpointLine(ax1, ay1, ax2, ay2, zone)

def circlePoints(x, y, cx, cy):
    setPixel(x + cx, y + cy)  # Zone 1
    setPixel(y + cx, x + cy)  # Zone 0
    setPixel(-x + cx, y + cy)  # Zone 2
    setPixel(-y + cx, x + cy)  # Zone 3
    setPixel(-y + cx, -x + cy)  # Zone 4
    setPixel(-x + cx, -y + cy)  # Zone 5
    setPixel(x + cx, -y + cy)  # Zone 6
    setPixel(y + cx, -x + cy)  # Zone 7

def MidpointCircle(radius, cx, cy):
    d = 1 - radius
    x = 0
    y = radius
    circlePoints(x, y, cx, cy)
    while x <= y:
        if d < 0:
            d = d + 2 * x + 3
            x += 1
        else:
            d = d + 2 * (x - y) + 5
            x += 1
            y -= 1
        circlePoints(x, y, cx, cy)

def drawControlButtons():
    glColor3f(0.0, 0.0, 0.0)
    drawButton(restart_button_x, restart_button_y, "<-",[1.0,1.0,1.0])
    glColor3f(0.0, 0.0, 0.0)
    drawButton(play_pause_button_x, play_pause_button_y, "|>" if paused else "||", [1.0,0.74,0.0])
    glColor3f(0.0, 0.0, 0.0)
    drawButton(terminate_button_x, terminate_button_y, "X",[1.0,0.0,0.0])

def drawButton(x, y, label,color):
    
    for i in range(buttonWidth):
        midpointLineEightWay(x + i, y, x + i, y + buttonHeight)
    glColor3f(color[0],color[1],color[2])
    glRasterPos2f(x + 10, y + 20)
    for char in label:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def generateCircles(value):
    global falling_circles, gameOver, paused
    if not gameOver and not paused:
        is_unique = random.random() < 0.1 #10% odds
        circle_data = [random.randint(70, screenWidth - 70), screenHeight]
        if is_unique:
            circle_data = [circle_data[0], circle_data[1], True, circle_radius]
        falling_circles.append(circle_data)
    glutTimerFunc(2000, generateCircles, 0)


def hasCollided(box1, box2):
    return (
        box1[0] < box2[0] + box2[2] and
        box1[0] + box1[2] > box2[0] and
        box1[1] < box2[1] + box2[3] and
        box1[1] + box1[3] > box2[1]
    )
def checkCollision():
    global gameOver, score
    rocket_box = [ship_x, ship_y, ship_width, ship_height]

    for circle in falling_circles:
        radius = circle[3] if len(circle) == 4 and circle[2] else circle_radius
        circle_box = [circle[0] - radius, circle[1] - radius, 2 * radius, 2 * radius]
        if hasCollided(rocket_box, circle_box):
            if len(circle) == 4 and circle[2]:  
                score += 10  
            gameOver = True
            break



def update(value):
    global ship_x, ship_y, falling_circles, falling_circles_speed, score, missed_circles, gameOver, projectliles
    if gameOver:
        glutTimerFunc(16, update, 0)
        return

    checkCollision()


    temp = []
    for circle in falling_circles:
        if len(circle) == 4 and circle[2]:  
            circle[3] += random.choice([-1, 1])
            circle[3] = max(5, min(20, circle[3])) 
        circle[1] -= falling_circles_speed  
        if circle[1] + circle_radius >= 0:
            temp.append(circle)
        else:
            missed_circles += 1
    falling_circles = temp



    temp = []
    for px, py in projectliles:
        py += 10 
        if py < screenHeight: 
            temp.append([px, py])
    projectliles = temp


    
    for px, py in projectliles:
        for circle in falling_circles:
            fx,fy = circle[0], circle[1]
            if ((px - fx) ** 2 + (py - fy) ** 2) ** 0.5 <= circle_radius + 5:
                projectliles.remove([px, py])
                if len(circle) == 4 and circle[2]:  
                    if circle[0] == fx and circle[1] == fy:
                        score += 5
                else:                       
                    score += 1
                print("Score: ",score)
                falling_circles.remove(circle)
                

    if missed_circles >= 3:
        gameOver = True
    glutPostRedisplay()
    glutTimerFunc(16,update,0)
    

def keyboardListener(key,x,y):
    global ship_x, gameOver,projectliles, paused

    if gameOver or paused:
        return
    
    if key == b'a':
        ship_x = max(50, ship_x - 10)
    elif key == b'd':
        ship_x = min(screenWidth-ship_width, ship_x + 10)
    if key == b' ':
        projectliles.append([ship_x+50, ship_y+150])

def mouseListener(button, state, x, y):
    global paused, score, gameOver, falling_circles, projectliles, missed_circles, falling_circles_speed

    y = screenHeight - y

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if restart_button_x <= x <= restart_button_x + buttonWidth and restart_button_y <= y <= restart_button_y + buttonHeight:
            score = 0
            missed_circles = 0
            falling_circles_speed = 1
            falling_circles = []
            projectliles = []
            gameOver = False
            paused = False
            print("Starting Over")
        elif play_pause_button_x <= x <= play_pause_button_x + buttonWidth and play_pause_button_y <= y <= play_pause_button_y + buttonHeight:
            paused = not paused
            if paused:
                falling_circles = []
                projectliles = []
        elif terminate_button_x <= x <= terminate_button_x + buttonWidth and terminate_button_y <= y <= terminate_button_y + buttonHeight:
            gameOver = True
            glClear(GL_COLOR_BUFFER_BIT)
            print(f"Goodbye. Final Score: {score}")
            glColor3f(1.0, 0.0, 0.0)
            glRasterPos2f(screenWidth // 2 - 60, screenHeight // 2)
            for char in "GAME OVER!!" + "Final Score: " + str(score):
             glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
            glutSwapBuffers()
            
            
            


def drawRocket(x,y):
    
    midpointLineEightWay(x,y,x+100,y)
    midpointLineEightWay(x+100,y,x+100,y+100)
    midpointLineEightWay(x+100,y+100,x,y+100)
    midpointLineEightWay(x,y+100,x,y)

    midpointLineEightWay(x,y+100,x+50,y+150)
    midpointLineEightWay(x+50,y+150,x+100,y+100)

    midpointLineEightWay(x,y,x-50,y)
    midpointLineEightWay(x-50,y,x,y+30)
    midpointLineEightWay(x+100,y,x+150,y)
    midpointLineEightWay(x+150,y,x+100,y+30)
    
def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, screenWidth, 0, screenHeight)

def display():
    global ship_x, ship_y, falling_circles, score, missed_circles, gameOver
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)

    if gameOver:
        glColor3f(1.0, 0.0, 0.0)
        glRasterPos2f(screenWidth // 2 - 60, screenHeight // 2)
        for char in "GAME OVER!!" + "Final Score: " + str(score):
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
        glutSwapBuffers()
        return

    drawRocket(ship_x, ship_y)

    for circle in falling_circles:
        radius = circle[3] if len(circle) == 4 and circle[2] else circle_radius
        if len(circle) == 4 and circle[2]:
            glColor3f(1.0, 0.5, 0.0)  
        else:
            glColor3f(1.0, 1.0, 1.0)  
        MidpointCircle(radius, circle[0], circle[1])
    for px, py in projectliles:
        glColor3f(1.0, 1.0, 1.0)  
        MidpointCircle(5, px, py)  


    drawControlButtons()
    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(screenWidth, screenHeight)
glutCreateWindow(b"Rocket Game")
init()
glutDisplayFunc(display)
glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouseListener)
glutTimerFunc(0, update, 0)
glutTimerFunc(2000, generateCircles, 0)
glutMainLoop()