
import turtle
import math
import random

class screensetup:
    screen = turtle.Screen()
    screen.setup(500,500)
    screen.setworldcoordinates(0,0,200.0,200.0)
    screen.tracer(0)  
    turtle.speed(0) 
    turtle.hideturtle()

class tanks:
    def __init__(self,x,y,angle,size,v,health,color,targetx,targety,rotate):
        self.x=x
        self.y=y
        self.size=size
        self.angle=angle
        self.v=v
        self.health=health
        self.color=color
        self.targetx=targetx
        self.targety=targety
        self.rotate=rotate

    def draw(self):
        turtle.color(self.color)
        turtle.pu()
        turtle.goto(self.x,self.y-self.size)
        turtle.pd()
        turtle.setheading(0)
        turtle.circle(self.size)
        turtle.pu()
        turtle.goto(self.x,self.y)
        turtle.pd()
        turtle.goto(self.x+math.cos(self.angle)*self.size * 1.5,self.y+math.sin(self.angle)*self.size *1.5)
               
    def move(self, tanks):
        tempX = self.x + math.cos(self.angle)*self.v # Get current X coordinate
        tempY = self.y + math.sin(self.angle)*self.v # Get current Y coordinate

        # Check for collisions with tanks
        for tank in tanks:
            if tank is not self:
                distance = math.sqrt((tempX-tank.x)**2 + (tempY-tank.y)**2)
                if distance < (self.size + tank.size):
                    # Collision occurred - stop the tanks
                    self.v = 0
                    self.rotate = 0
                    tank.v = 0
                    tank.rotate = 0
                    return

        # Check for collisions with walls
        if (tempX > 0.0 and tempX < 200.0) and (tempY > 0.0 and tempY < 200.0):
            self.x = tempX
            self.y = tempY
            self.angle += self.rotate
        else:
            # Collision occurred - stop the tank in the direction of the wall
            if tempX <= 0.0 or tempX >= 200.0:
                self.rotate = -self.rotate
            if tempY <= 0.0 or tempY >= 200.0:
                self.rotate = -self.rotate
            self.v = 0

    def target(self, x,y):
        self.targetx=x
        self.targety=y

    def ai(self):
        self.angle = math.atan2(self.y - self.targety, self.x - self.targetx) * (180 / 3.14)

    def controlrotation(self,rotate):
        self.rotate=rotate

    def controlvelocity(self,velocity):
        self.v=velocity    

class keyboard:
    def __init__(self,tank):
        keyboard.tank = tank
        keyboard.end=0
        screensetup.screen.listen() 
        screensetup.screen.onkeypress(self.kmove, "Up") 
        screensetup.screen.onkeyrelease(self.kstop, "Up")
        screensetup.screen.onkeypress(self.kleft, "Left")
        screensetup.screen.onkeyrelease(self.kleftstop, "Left")
        screensetup.screen.onkeypress(self.kright, "Right")
        screensetup.screen.onkeyrelease(self.krightstop, "Right")
        screensetup.screen.onkeypress(self.kend, "Escape")
    def kmove(self):  
        keyboard.tank.controlvelocity(.2)
    def kstop(self):
        keyboard.tank.controlvelocity(0)
    def kleft(self):
        keyboard.tank.controlrotation(.02)
    def kleftstop(self):
        keyboard.tank.controlrotation(0)
    def kright(self):
        keyboard.tank.controlrotation(-.02)
    def krightstop(self):
        keyboard.tank.controlrotation(0)
    def kend(self):
        keyboard.end=1

user=tanks(10,10,0,5,0,10,"blue",0,0,0)
keyboard(user)

numtanks= 4
enemy = [] 
for i in range(numtanks):    
    enemy+=[tanks(random.randint(5,195),random.randint(5,195),random.randint(0,360),5,0.15,10,"red",0,0,0)]

while not keyboard.end: 
    turtle.clear()

    # Move and draw enemy tanks; allows each enemy tank to check for collisions 
    # with all the other tanks in the game, including the user tank
    for i in enemy:
        i.target(user.x,user.y)
        i.move(enemy+[user])
        i.ai()
        i.draw()

    # Move and draw user tank; allows the user tank to check for collisions 
    # with all the enemy tanks, in addition to checking for collisions with the walls.
    user.move(enemy+[user])
    user.draw()

    screensetup.screen.update()         
     
