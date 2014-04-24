# Implementation of classic arcade game Pong
# by Pav31
# http://www.codeskulptor.org/#user30_q2i49coPndadcS1.py

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

sound_side = simplegui.load_sound("http://pav31.com/coursera/pong-game/sounds/paddle.mp3")
sound_score = simplegui.load_sound("http://pav31.com/coursera/pong-game/sounds/score.mp3")
sound_paddle = simplegui.load_sound("http://pav31.com/coursera/pong-game/sounds/side.mp3")

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    sound_score.rewind()
    sound_score.play()

    # Assign random velocity
    ball_vel = [-random.randrange(120, 240) / 60, \
                -random.randrange(60, 180) / 60]
    # Flip direction if LEFT
    if direction == RIGHT:
        ball_vel[0] *= -1

def score(side):
    '''Updates score'''
    global score1, score2
    if side == LEFT:
        score1 += 1
    else:
        score2 += 1


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints

    paddle1_vel = [0, 0]
    paddle2_vel = [0, 0]
    ball_pos = [WIDTH / 2, HEIGHT / 2]

    paddle1_pos = [[HALF_PAD_WIDTH,HEIGHT / 2 - HALF_PAD_HEIGHT], \
                   [HALF_PAD_WIDTH, HEIGHT / 2 + HALF_PAD_HEIGHT]]
    paddle2_pos = [[WIDTH - HALF_PAD_WIDTH,HEIGHT / 2 - HALF_PAD_HEIGHT], \
                   [WIDTH - HALF_PAD_WIDTH, HEIGHT / 2 + HALF_PAD_HEIGHT]]

    if random.randrange(2) == 0:
        spawn_ball(RIGHT)
    else:
        spawn_ball(LEFT)
    score1 = 0
    score2 = 0


def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # Update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")

    # Reflect vertical left
    if ball_pos[0] - BALL_RADIUS <= PAD_WIDTH:
        # If ball hit the paddle1
        if (paddle1_pos[0][1] <= ball_pos[1] <= paddle1_pos[1][1]):
            sound_paddle.play()
            ball_vel[0] *= -1.1
        else:
            score(RIGHT)
            spawn_ball(RIGHT)

    elif ball_pos[0] + BALL_RADIUS >= (WIDTH - 1) - PAD_WIDTH:
        # If ball hit the paddle1 or paddle2
        if (paddle2_pos[0][1] <= ball_pos[1] <= paddle2_pos[1][1]):
            sound_paddle.play()
            ball_vel[0] *= -1.1
        else:
            score(LEFT)
            spawn_ball(LEFT)

    # Reflect horizontal
    if ball_pos[1] <= BALL_RADIUS or\
    ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS:
        sound_side.play()
        ball_vel[1] = -ball_vel[1]

    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos[0][1] += paddle1_vel[1]
    paddle1_pos[1][1] += paddle1_vel[1]
    paddle2_pos[0][1] += paddle2_vel[1]
    paddle2_pos[1][1] += paddle2_vel[1]

    if paddle1_pos[0][1] < 0 or paddle1_pos[0][1] > HEIGHT - PAD_HEIGHT:
        paddle1_pos[0][1] -= paddle1_vel[1]
        paddle1_pos[1][1] -= paddle1_vel[1]
    if paddle2_pos[0][1] < 0 or paddle2_pos[0][1] > HEIGHT - PAD_HEIGHT:
        paddle2_pos[0][1] -= paddle2_vel[1]
        paddle2_pos[1][1] -= paddle2_vel[1]

    # draw paddles
    canvas.draw_line(paddle1_pos[0],paddle1_pos[1], PAD_WIDTH, "White")
    canvas.draw_line(paddle2_pos[0],paddle2_pos[1], PAD_WIDTH, "White")
    # draw scores
    canvas.draw_text(str(score1), [WIDTH/2 - 120, 100], 80, "White")
    canvas.draw_text(str(score2), [WIDTH/2 + 80, 100], 80, "White")


def keydown(key):
    global paddle1_vel, paddle2_vel
    acc = 8

    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel[1] -= acc
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel[1] += acc
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel[1] -= acc
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel[1] += acc


def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"] or\
    key == simplegui.KEY_MAP["s"]:
        paddle1_vel[1] = 0
    elif key == simplegui.KEY_MAP["up"] or\
    key == simplegui.KEY_MAP["down"]:
        paddle2_vel[1] = 0


def reset():
    '''Reset Button'''
    new_game()

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.add_button('New game', reset, 200)
frame.add_label("")
frame.add_label('Left Paddle: W | S', 80)
frame.add_label("")
frame.add_label("Right Paddle: Up | Down", 100)

frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# start frame
new_game()
frame.start()
