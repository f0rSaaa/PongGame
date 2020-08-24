import sys, pygame, random
from pygame import gfxdraw

pygame.init()
clock = pygame.time.Clock()

#screen
screen_width = 480
screen_height = 320
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PongPongPOng")

background = pygame.image.load('bg.png')

#character 

ball = pygame.Rect(screen_width // 2 - 5, screen_height // 2 - 5 , 10 , 10)
player = pygame.Rect(30, screen_height // 2 - 20 , 5 , 40)
opponent = pygame.Rect(screen_width - 35, screen_height // 2 - 20 , 5 , 40)

ball_speed_x = 4 * random.choice((1,-1))
ball_speed_y = 4 * random.choice((1,-1))
player_speed = 0
opponent_speed = 7 

run = True

#drawing window
def drawWindow():
    win.blit(background, (0,0))
    pygame.draw.rect(win,(255,255,255), player)
    pygame.draw.rect(win,(255,255,255), opponent)
    pygame.draw.ellipse(win, (255, 255, 255), ball)
    pygame.display.update()

def ball_animation():
    global ball_speed_x, ball_speed_y
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <=0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    if ball.left <=0 or ball.right >= screen_width:
        ball_restart()

    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1

def player_animation():
    player.y += player_speed

    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_movement():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y: 
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

def ball_restart():
    global ball_speed_x, ball_speed_y
    ball.center = (screen_width/2, screen_height/2)
    ball_speed_x *= random.choice((1,-1))
    ball_speed_y *= random.choice((1,-1))

#main loop
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 5
            if event.key == pygame.K_UP:    
                player_speed -= 5 
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 5
            if event.key == pygame.K_UP:    
                player_speed += 5 

    ball_animation()
    player_animation()
    opponent_movement()
    drawWindow()
    clock.tick(60)

pygame.quit()
sys.exit()