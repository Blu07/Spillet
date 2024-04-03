import turtle
import numpy as np
import keyboard as kb

def drawingTurtle(pos, color="#000000"):
    global drawer

    drawer.color = color
    drawer.speed(10)
    drawer.penup()
    drawer.goto(pos)
    drawer.pendown()

    return drawer


def drawLine(start=(0, 0), end=(100, 0)):
    lineDrawer = drawingTurtle(start, "#00ff00")
    lineDrawer.goto(end)

def drawDot(pos):
    dotDrawer = drawingTurtle(pos)
    dotDrawer.dot(4, "#0000ff")


class Base:
    def __init__(self, x: int=0, y: int=0, child=None) -> None:
        self.child = child
        self.hasChild = True if child else False
        self.pos = np.array([x, y])

    def setChild(self, child):
        self.child = child
        self.hasChild = True

    def draw(self):
        # Draw own dot
        drawDot(self.pos)

    def updatePos(self, *args, **kwargs):
        pass

    


class Joint(Base): ...
class Joint(Base):
    def __init__(self, x: int, y: int, parent: Joint, child: Joint=None) -> None:
        super().__init__(x=x, y=y, child=child)
        self.parent = parent
        
        self.weight = 4

        self.speed = np.array([0, 0])
        self.acceleration = np.array([0, 0])

        if not self.parent.hasChild:
            self.parent.setChild(self)

    def draw(self):
        # Draw own dot
        drawDot(self.pos)
        # Draw to Parent
        drawLine(self.pos, self.parent.pos)
    
    def updatePos(self):
        pass


       

class Circle:
    
    
    def __init__(self, r, m, initPos=[0, 0], initVel=[0, 0], initAcc=[0, 0]) -> None:
        self.radius = r
        self.mass = m
        
        self.gravity = np.array([0, -9.8], dtype=np.float64)
        self.pos = np.array(initPos, dtype=np.float64)
        self.vel = np.array(initVel, dtype=np.float64)
        self.acc = np.array(initAcc, dtype=np.float64)

    def update(self, dt):
        if self.pos[1] < -200:
            self.vel[1] *= -1
        
        self.acc += self.gravity  # Add gravity to acceleration
        self.vel += self.acc * dt  # Update velocity by adding acceleration
        self.pos += self.vel * dt
        
        
    def draw(self):
        # Draw circle on screen
        drawDot(self.pos)

    def addVel(self, velocityChange):
        self.vel += np.array(velocityChange, dtype=np.float64)
        print(self.vel)
        print("added Vel:", velocityChange)
    
    def setVel(self, velocityChange):
        self.vel = np.array(velocityChange, dtype=np.float64)



def update():
    drawer.clear()
    # ---
    dt = 0.01
    myCircle.update(dt)
    myCircle.draw()

    # ---
    screen.update()
    turtle.ontimer(update, int(1000*dt))



if __name__ == "__main__":

    screen = turtle.Screen()
    screen.setup(600, 800)
    screen.bgcolor("#222222")
    screen.tracer(0)

    drawer = turtle.Turtle()
    drawer.ht()

    myCircle = Circle(4, 2)

    kb.add_hotkey("f", lambda: myCircle.setVel([0, 300]))


    update()

    # pendulumBase = Base()
    # joint1 = Joint(-100, 0, pendulumBase)
    # joint2 = Joint(100, -200, joint1)
    # joint3 = Joint(0, -300, joint2)

    # pendulum = [pendulumBase, joint1]#, joint2, joint3]
    # dt = 50
    # update()

    turtle.done()