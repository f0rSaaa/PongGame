import sys, pygame, random
from pygame import gfxdraw


pygame.mixer.pre_init(44100, -16, 2, 512)
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
opponent = pygame.Rect(screen_width - 35, screen_height // 2 - 20 , 5, 40) #5

ball_speed_x = 4 * random.choice((1,-1))
ball_speed_y = 4 * random.choice((1,-1))
player_speed = 0
opponent_speed = 7 

#sounds 
pong_sound = pygame.mixer.Sound("pong.ogg")
pong_sound.set_volume(0.1)
score_sound = pygame.mixer.Sound("score.ogg")
score_sound.set_volume(0.1)

#background music 
pygame.mixer.music.load("melodyloops-preview-happy-place-2m30s.mp3")
pygame.mixer.music.set_volume(0.03)
pygame.mixer.music.play(-1)

#scores -- Text variables
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf",16)
game_font_timer = pygame.font.Font("freesansbold.ttf",96)

#score timer
score_time = True

run = True

#drawing window
def drawWindow():
    win.blit(background, (0,0))
    pygame.draw.rect(win,(255,255,255), player)
    pygame.draw.rect(win,(255,255,255), opponent)
 
    player_text = game_font.render(f"{player_score}", True, (255, 255, 255))
    win.blit(player_text, (220, 25))
    opponent_text = game_font.render(f"{opponent_score}", True, (255, 255, 255))
    win.blit(opponent_text, (253, 25))
    pygame.draw.ellipse(win, (255, 255, 255), ball)

    pygame.display.update()

#drawing timer
def draw_timer_score(number):
    number_to_print = game_font_timer.render(f"{number}", True, (211, 211, 211))
    win.blit(number_to_print, (screen_width // 2 - 25 , screen_height // 2 - 40))
    pygame.display.update()

#ball animation
def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <=0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
        pygame.mixer.Sound.play(pong_sound)

    #opponent score
    if ball.left <=0:
        pygame.mixer.Sound.play(score_sound)
        opponent_score += 1
        score_time = pygame.time.get_ticks()

    #player score
    if ball.right >= screen_width:
        pygame.mixer.Sound.play(score_sound)
        player_score += 1
        score_time = pygame.time.get_ticks()

    if ball.colliderect(player) and ball_speed_x < 0:
        pygame.mixer.Sound.play(pong_sound) 

        if abs(ball.left - player.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:   #ball_speed_y > 0:  condition to check moving downward
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:   #ball_speed_y < 0:  condition to check moving upward
            ball_speed_y *= -1


    if ball.colliderect(opponent) and ball_speed_x > 0:
        pygame.mixer.Sound.play(pong_sound)

        if abs(ball.right - opponent.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

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
    global ball_speed_x, ball_speed_y, score_time
    
    current_time = pygame.time.get_ticks()
    ball.center = (screen_width/2, screen_height/2)

    if current_time - score_time < 700:
        draw_timer_score(3)
    if  700 <current_time - score_time < 1400:
        draw_timer_score(2)
    if  1400 <current_time - score_time < 2100:
        draw_timer_score(1)
    
    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        ball_speed_x = 4 * random.choice((1,-1))
        ball_speed_y = 4 * random.choice((1,-1))
        score_time = None

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

    if score_time:
        ball_restart()

    clock.tick(60)

pygame.quit()
sys.exit()