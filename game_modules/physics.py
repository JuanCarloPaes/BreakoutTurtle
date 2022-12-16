from math import cos, radians, sin

base_speed = 0.4


def calculate_angle(ball, degrees):
    dx = base_speed * cos(radians(degrees))
    dy = base_speed * sin(radians(degrees))
    ball.dx = round(dx, 2)
    ball.dy = round(dy, 2)


def collision(paddle, ball):
    px, py = paddle.xcor(), paddle.ycor()
    bx, by = ball.xcor(), ball.ycor()

    paddle_sizes = paddle.shapesize()
    paddle_half_height = paddle_sizes[0] * 10
    paddle_half_width = paddle_sizes[1] * 10

    ball_radius = ball.shapesize()[0] * 10

    if (px - paddle_half_width <= bx <= px + paddle_half_width and
            by - ball_radius <= py + paddle_half_height and by - 10 >= py -
            paddle_half_height):
        degrees = px - bx + 90
        calculate_angle(ball, degrees)
        ball.goto(bx + ball.dx, py + paddle_half_height + ball_radius)
        return True

    if py + paddle_half_height >= by >= py - paddle_half_height and \
            ((bx + ball_radius >= px - paddle_half_width and bx < px) or
             (bx - ball_radius <= px + paddle_half_width and bx > px)):
        ball.dx *= -1
        ball.dy *= -1
        if bx < px:
            ball.goto(px - paddle_half_width - ball_radius, by + ball.dy)
        else:
            ball.goto(px + paddle_half_width + ball_radius, by + ball.dy)
        return True
    return False


def collision_brick(brick, ball):
    brx, bry = brick.xcor(), brick.ycor()
    bx, by = ball.xcor(), ball.ycor()
    if brick.isvisible():
        if brx - 40 < bx < brx + 40:
            if ((by - 10 <= bry + 10 and by > bry) or
                    (by + 10 >= bry - 10 and by < bry)):
                ball.dy *= -1
                return True
        if bry + 10 > by > bry - 10:
            if (brx - 40 <= bx < brx) or (brx + 40 >= bx > brx):
                ball.dx *= -1
                ball.dy *= -1
                return True
    return False
