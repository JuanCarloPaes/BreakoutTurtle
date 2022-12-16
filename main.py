from random import randint
from time import sleep
import turtle
from game_modules import physics, sounds, utils, objects

ball_initial_position_x = 0
ball_initial_position_y = -220
playing = True
is_rolling = True


def close_screen():
    global playing
    playing = not playing


screen = objects.create_screen("Breakout", 800, 600)

# draw block
y = 200
for color in utils.colors.keys():
    objects.create_line_of_bricks(y, color)
    y -= 30

paddle = objects.create_paddle(0, -250, 0.8, 6, "white")
ball = objects.create_ball(ball_initial_position_x, ball_initial_position_y, "white")

# starting speed
if randint(0, 1) == 0:
    ball.dx = physics.base_speed
else:
    ball.dx = -physics.base_speed
ball.dy = 0


# move left
def paddle_left():
    x = paddle.xcor()
    if x > -350:
        x += -30
    else:
        x = -350
    paddle.setx(x)
    if is_rolling:
        ball.setx(ball.xcor() - 30)


# move right
def paddle_right():
    x = paddle.xcor()
    if x < 350:
        x += 30
    else:
        x = 350
    paddle.setx(x)
    if is_rolling:
        ball.setx(ball.xcor() + 30)


# throw ball
def throw_ball():
    global is_rolling
    if is_rolling:
        px = paddle.xcor()
        bx = ball.xcor()
        degrees = px - bx + 90
        physics.calculate_angle(ball, degrees)
        is_rolling = False


# keyboard
screen.listen()
screen.onkeypress(paddle_right, "Right")
screen.onkeypress(paddle_left, "Left")
screen.onkeypress(throw_ball, "space")
score_hud = objects.create_hud(-250, 250)
lifes_hud = objects.create_hud(300, 250)
lifes_hud.color("red")


def update_hud():
    score_hud.clear()
    score_hud.write("SCORE {}".format(utils.score), align="center",
                    font=("Press Start 2P", 18, "normal"))
    lifes_hud.clear()
    # hearts
    lifes_hud.write("\u2764" * utils.lifes, align="center",
                    font=("Press Start 2P", 24, "normal"))


update_hud()
while playing:

    # stop game
    if utils.lifes == 0:
        update_hud()
        objects.end_game_screen("GAME OVER :(")
        sounds.play_defeat()
        sleep(2)
        playing = False
        continue
    if utils.inv_bricks == 28:
        update_hud()
        objects.end_game_screen("YOU WIN :)")
        sounds.play_victory()
        sleep(2)
        playing = False
        continue

    # movement
    if is_rolling:
        ball.setx(ball.xcor() + ball.dx)
        paddle_half_width = paddle.shapesize()[1] * 10
        if ball.xcor() + 10 >= paddle.xcor() + paddle_half_width or \
                ball.xcor() - 10 <= paddle.xcor() - paddle_half_width:
            ball.dx *= -1
    else:
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)
    if physics.collision(paddle, ball):
        sounds.play_bounce()

    for brick in objects.bricks:
        if physics.collision_brick(brick, ball):
            sounds.play_bounce()
            brick.hideturtle()
            utils.inv_bricks += 1
            utils.update_score(brick.color()[0])
            update_hud()
    # collision right
    if ball.xcor() > 385:
        sounds.play_bounce()
        ball.setx(385)
        ball.dx *= -1
    # collision left
    if ball.xcor() < -388:
        sounds.play_bounce()
        ball.setx(-388)
        ball.dx *= -1
    # collision up
    if ball.ycor() > 288:
        sounds.play_bounce()
        ball.dy *= -1
    # reset
    if ball.ycor() < -300:
        utils.lifes -= 1
        update_hud()
        ball.goto(paddle.xcor(), ball_initial_position_y)
        ball.dx = physics.base_speed
        ball.dy = 0
        is_rolling = True
        # random start
        if randint(0, 1) == 0:
            ball.dx *= -1
    screen.update()
