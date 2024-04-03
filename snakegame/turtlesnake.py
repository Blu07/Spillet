
import turtle, keyboard, time, random, math


window = turtle.Screen()
window.title("Vill ass snake spill YEYE!")
window.bgcolor("#000000")


retro_graphics = True

player = turtle.Turtle()
player.shape("square")
player.shapesize(0.8)
player.color("#000000")
player.speed(0)
player.penup()

apple = turtle.Turtle()
apple.shape("square")
apple.shapesize(0.6)
apple.color("#a60202")
apple.speed(0)
apple.penup()
apple.hideturtle()

map = turtle.Turtle()
map.speed(0)
map.hideturtle()
map.penup()
map.pensize(3)

writer = turtle.Turtle()
writer.color("#ffffff")
writer.pensize(2)
writer.ht()
writer.pu()

border_x = 0
border_y = 0
with_multiplier = 40
height_multiplier = 20
winning_score = 0

player_speed = 20
game = True
player_direction_x = player_speed
player_segments_pos = []
player_direction_y = 0
player_segments = []
player_score = 0
player_turning = False

with open('snakegame/highscore.txt', 'r') as f:
    highscore = int(f.read())

def create_map(width, height, border_color, fill_color, background_color):
    global border_x, border_y, with_multiplier, height_multiplier, winning_score
    winning_score = width * height - 4
    writer.goto(width * with_multiplier * -1 - 10, height * height_multiplier + 60)
    border_x = width * with_multiplier + 10
    border_y = height * height_multiplier + 10
    window.bgcolor(background_color)
    map.color(border_color)
    map.fillcolor(fill_color)
    map.goto(width * with_multiplier * -1 - 10, height * height_multiplier + 10)
    map.pendown()
    map.begin_fill()
    for _ in range(2):
        map.forward(width * with_multiplier * 2 + 20)
        map.right(90)
        map.forward(height * height_multiplier * 2 + 20)
        map.right(90)
    map.end_fill()
    map.penup()

def write_score():
    global player_score, border_x, border_y, highscore
    writer.clear()
    writer.goto(-border_x, border_y + 80)
    writer.write(f"Highscore: {highscore}", align="left", font=("Arial", 16, "normal"))
    writer.goto(-border_x, border_y + 50)
    writer.write(f"Score: {player_score}", align="left", font=("Arial", 16, "normal"))

def place_apple():
    global border_x, border_y, with_multiplier, height_multiplier
    apple.hideturtle()
    apple_x = random.randint(int((border_x-10)/with_multiplier * -1), int((border_x-10)/with_multiplier)) * 20
    apple_y = random.randint(int((border_y-10)/height_multiplier * -1), int((border_y-10)/height_multiplier)) * 20
    apple.goto(apple_x, apple_y)
    while apple.pos() in player_segments_pos:
        apple_x = random.randint(int((border_x-10)/with_multiplier * -1), int((border_x-10)/with_multiplier)) * 20
        apple_y = random.randint(int((border_y-10)/height_multiplier * -1), int((border_y-10)/height_multiplier)) * 20
        apple.goto(apple_x, apple_y)
    apple.showturtle()

def player_move():
    global player_direction_x, player_direction_y, player_turning
    plx = player_direction_x
    ply = player_direction_y
    for i in [1,2]:
        player.goto(player.xcor() + plx/2, player.ycor() + ply/2)
        player_segments.append(player.stamp())
        player_segments_pos.append(player.pos())
    if len(player_segments) >= player_score + 8:
        player.clearstamp(player_segments.pop(0))
        player_segments_pos.pop(0)
        player.clearstamp(player_segments.pop(0))
        player_segments_pos.pop(0)
    player_turning = False

def player_eating():
    global player_score, highscore, winning_score
    if player.distance(apple) < 20:
        player_score += 1
        place_apple()
        if player_score > highscore:
            highscore = player_score
            with open('snakegame/highscore.txt', 'w') as f:
                f.write(str(player_score))
        write_score()
    if player_score >= winning_score:
        game = False

def check_collision():
    global game, border_x, border_y, player_segments_pos
    if player.xcor() not in range(-border_x, border_x):
        game = False
    if player.ycor() not in range(-border_y, border_y):
        game = False
    if player.pos() in player_segments_pos[:-1]:
        game = False

def player_up(event):
    global player_direction_x, player_direction_y, player_speed, player_turning
    if event.name == "w" and player_direction_y >= 0 and not player_turning:
        player_turning = True
        player_direction_x = 0
        player_direction_y = player_speed

def player_down(event):
    global player_direction_x, player_direction_y, player_speed, player_turning
    if event.name == "s" and player_direction_y <= 0 and not player_turning:
        player_turning = True
        player_direction_x = 0
        player_direction_y = -player_speed

def player_left(event):
    global player_direction_x, player_direction_y, player_speed, player_turning
    if event.name == "a" and player_direction_x <= 0 and not player_turning:
        player_turning = True
        player_direction_x = -player_speed
        player_direction_y = 0

def player_right(event):
    global player_direction_x, player_direction_y, player_speed, player_turning
    if event.name == "d" and player_direction_x >= 0 and not player_turning:
        player_turning = True
        player_direction_x = player_speed
        player_direction_y = 0

keyboard.on_press_key("w", player_up)
keyboard.on_press_key("s", player_down)
keyboard.on_press_key("a", player_left)
keyboard.on_press_key("d", player_right)

if retro_graphics:
    create_map(10, 13, "#ffffff", "#000000", "#000000")
    player.color("#ffffff")
    apple.color("#ffffff")
else:
    create_map(10, 13, "#000000", "#2b5c1d", "#120d08")

place_apple()
write_score()

while game:
    player_move()
    check_collision()
    player_eating()
    time.sleep(0.1)

writer.goto(0, border_y + 40)
if player_score >= winning_score:
    writer.write("GAME WON!", align="center", font=("Arial", max(math.floor((border_x-10)/with_multiplier*4), 16), "normal"))
else:
    writer.write("GAME OVER!", align="center", font=("Arial", max(math.floor((border_x-10)/with_multiplier*4), 16), "normal"))

turtle.done()

