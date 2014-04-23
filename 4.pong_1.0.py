# Implementation of classic arcade game Pong

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

snd_boom–boom = "https://github.com/pav31/Pong-game/blob/master/sounds/boom–boom.mp3"
snd_borders = "https://github.com/pav31/Pong-game/blob/master/sounds/borders.mp3"
snd_paddle1 = "https://github.com/pav31/Pong-game/blob/master/sounds/paddle1.mp3"
snd_paddle2 = "https://github.com/pav31/Pong-game/blob/master/sounds/paddle2.mp3"
snd_score = "https://github.com/pav31/Pong-game/blob/master/sounds/score.mp3"
snd_side = "https://github.com/pav31/Pong-game/blob/master/sounds/side.mp3"

paddle1_pos = [[HALF_PAD_WIDTH,HEIGHT / 2 - HALF_PAD_HEIGHT], \
               [HALF_PAD_WIDTH, HEIGHT / 2 + HALF_PAD_HEIGHT]]
paddle2_pos = [[WIDTH - HALF_PAD_WIDTH,HEIGHT / 2 - HALF_PAD_HEIGHT], \
               [WIDTH - HALF_PAD_WIDTH, HEIGHT / 2 + HALF_PAD_HEIGHT]]

ball_pos = [WIDTH / 2, HEIGHT / 2]
paddle1_vel = [0, 0]
paddle2_vel = [0, 0]

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]

    # Assign random velocity
    # ??? DOUBLE CHECK DEVISION
    # Signs are GOOD


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
    if random.randrange(2) == 0:
        spawn_ball(RIGHT)
    else:
        spawn_ball(LEFT)
    score1 = 0
    score2 = 0


def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel

    # draw mid line and gutters
    #  # GOOD!!!
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # Update ball position
    #  # GOOD!!!
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Draw ball
    #  # GOOD!!!
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")

    # Reflect vertical left
    #  # GOOD!!!
    if ball_pos[0] - BALL_RADIUS <= PAD_WIDTH:
        # If ball hit the paddle1
        if (paddle1_pos[0][1] <= ball_pos[1] <= paddle1_pos[1][1]):
            play_sound(paddle1)
            ball_vel[0] *= -1.1
        else:
            play_sound(score)
            score(RIGHT)
            spawn_ball(RIGHT)
    elif ball_pos[0] + BALL_RADIUS >= (WIDTH - 1) - PAD_WIDTH:
        # If ball hit the paddle1 or paddle2
        if (paddle2_pos[0][1] <= ball_pos[1] <= paddle2_pos[1][1]):
            play_sound(paddle2)
            ball_vel[0] *= -1.1
        else:
            play_sound(score)
            score(LEFT)
            spawn_ball(LEFT)

    # Reflect horizontal
    #  # GOOD!!!
    if ball_pos[1] <= BALL_RADIUS or\
    ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS:
        play_sound(side)
        ball_vel[1] = -ball_vel[1]

    # update paddle's vertical position, keep paddle on the screen
    #  # GOOD!!!
    paddle1_pos[0][1] += paddle1_vel[1]
    paddle1_pos[1][1] += paddle1_vel[1]

    paddle2_pos[0][1] += paddle2_vel[1]
    paddle2_pos[1][1] += paddle2_vel[1]

    if paddle1_pos[0][1] < 0 or paddle1_pos[0][1] > HEIGHT - PAD_HEIGHT:
        paddle1_pos[0][1] -= paddle1_vel[1]
        paddle1_pos[1][1] -= paddle1_vel[1]
        paddle1_vel[1] = 0
    if paddle2_pos[0][1] < 0 or paddle2_pos[0][1] > HEIGHT - PAD_HEIGHT:
        paddle2_pos[0][1] -= paddle2_vel[1]
        paddle2_pos[1][1] -= paddle2_vel[1]
        paddle2_vel[1] = 0
    # GOOD!!!

    # draw paddles
    #  # GOOD!!!
    canvas.draw_line(paddle1_pos[0],paddle1_pos[1], PAD_WIDTH, "White")
    canvas.draw_line(paddle2_pos[0],paddle2_pos[1], PAD_WIDTH, "White")
    # GOOD!!!

    # draw scores
    canvas.draw_text(str(score1), [WIDTH/2 - 85, 100], 100, "White")
    canvas.draw_text(str(score2), [WIDTH/2 + 37, 100], 100, "White")

# GOOD!!!
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


# GOOD!!!
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

def play_sound(url):
    '''Loads sound from url, plays it and rewinds'''
    sound = simplegui.load_sound(url)
    sound.play()
    sound.rewind()



 # GOOD!!!
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.add_label("")
frame.add_label("")
frame.add_label("")
frame.add_label("")
frame.add_label("")
frame.add_button('New game', reset, 200)
frame.add_label("")
frame.add_label("")
frame.add_label("")
frame.add_label("")
frame.add_label("")
frame.add_label("")
frame.add_label("Left paddle: W and S")
frame.add_label("")
frame.add_label("Right paddle: UP and DOWN")

frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
