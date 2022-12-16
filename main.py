import turtle as tr

# screen
screen = tr.Screen()
screen.setup(width=1200, height=900)
screen.bgcolor('black')
screen.title('Breakout')

# draw ball
ball = tr.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.shapesize(stretch_wid=0.5)
ball.penup()
ball.goto(0, 0)
ball.dx = 3
ball.dy = 3


while True:
    screen.update()
