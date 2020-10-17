import pygame
import random

pygame.init()

clock = pygame.time.Clock()
#variable declarations
speed = 30

display_width = 800
display_height = 500

x = 100
y = 100
radius = 10
dx = 3
dy = 3

paddle_width = 4
paddle_height = 40

paddle1_x = 10
paddle1_y = 10
paddle2_x = display_width - 10 - paddle_width
paddle2_y = 10


play_score1 = 0
play_score2 = 0
player1_is_current = False

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("PONG")

heading = pygame.font.SysFont("verdana", 36)
para = pygame.font.SysFont("verdana", 24)
instructions = pygame.font.SysFont("verdana", 18)

def randomise_start():
    global x, y, dy
    x = display_width // 2
    y = random.randint(10, display_height - 10)
    if random.randint(0, 2) % 2 == 0:
        dy *= -1

def hit_paddle():
    global play_score1, play_score2, speed
    if (player1_is_current):
        if x - radius <= paddle1_x + paddle_width:
            if y + radius > paddle1_y and y - radius < paddle1_y + paddle_height:
                play_score1 += 10
                speed += 1
                return 1
            else:
                return -1
    else:
        if x + radius >= paddle2_x:
            if y + radius > paddle2_y and y - radius < paddle2_y + paddle_height:
                play_score2 += 10
                speed += 1
                return 1
            else:
                return -1
    return 0

def hit_wall():
    if (y <= radius) or (y + radius >= display_height):
        return True
    return False

def game_over():
    global play_score1, play_score2
    screen.fill((0, 0, 0))

    if (play_score1 > play_score2):
        winner = "Player 1 wins!"
    elif (play_score1 == play_score2):
        winner = "Draw!"
    else:
        winner = "Player 2 wins!"

    gameover = heading.render(winner, True, (255, 255, 255))
    gameover_rect = gameover.get_rect(center = (display_width//2, display_height//2))
    screen.blit(gameover, gameover_rect)
    restart = instructions.render("Press r to Restart", True, (255, 255, 255))
    restart_rect = restart.get_rect(center = (display_width//2, display_height//1.5))
    screen.blit(restart, restart_rect)
    quit = instructions.render("Press q to Quit", True, (255, 255, 255))
    quit_rect = quit.get_rect(center = (display_width//2, display_height//1.3))
    screen.blit(quit, quit_rect)
    final_score = para.render("P1: " + str(play_score1) + "   P2:" + str(play_score2), True, (255, 255, 255))
    final_score_rect = final_score.get_rect(center = (display_width//2, display_height//4))
    screen.blit(final_score, final_score_rect)
    pygame.display.update()
    endgame = True
    while (endgame):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                if event.key == pygame.K_r:
                    endgame = False

#main game loop 
welcome = heading.render("Let's play Pong!", True, (255, 255, 255))
welcome_rect = welcome.get_rect(center = (display_width//2, display_height//3))
screen.blit(welcome, welcome_rect)
startmsg = instructions.render("Press y to start or auto-start in 10s.", True, (255, 255, 255))
startmsg_rect = startmsg.get_rect(center = (display_width//2, display_height//1.5))
screen.blit(startmsg, startmsg_rect)
pygame.display.flip()

pygame.time.set_timer(pygame.USEREVENT, 10000)

timer_active = True
while timer_active:
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:
            timer_active = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_y:
                timer_active = False

randomise_start()

while True:
    clock.tick(speed)
    
    pressed_key = pygame.key.get_pressed()
    if pressed_key[pygame.K_s]:
        if paddle_height + 10 + paddle1_y <= display_height:
            paddle1_y += 10
    if pressed_key[pygame.K_DOWN]:
        if paddle_height + 10 + paddle2_y <= display_height:
            paddle2_y += 10
    if pressed_key[pygame.K_w]:
        if paddle1_y - 10 >= 0:
            paddle1_y -= 10
    if pressed_key[pygame.K_UP]:
        if paddle2_y - 10 >= 0:
            paddle2_y -= 10

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    
    x += dx
    y += dy
    screen.fill((0, 0, 0))
    score1 = para.render("P1: " + str(play_score1), True, (255, 255, 255))
    score1_rect = score1.get_rect(topleft = (display_width // 4, 30))
    screen.blit(score1, score1_rect)
    score2 = para.render("P2: " + str(play_score2), True, (255, 255, 255))
    score2_rect = score2.get_rect(topleft = (display_width // 1.5, 30))
    screen.blit(score2, score2_rect)
    pygame.draw.rect(screen, (255, 255, 255), (paddle1_x, paddle1_y, paddle_width, paddle_height))
    pygame.draw.rect(screen, (255, 255, 255), (paddle2_x, paddle2_y, paddle_width, paddle_height))

    pygame.draw.circle(screen, (255, 255, 255), (x, y), radius)

    if(hit_wall()):
        dy *= -1
    flag = hit_paddle()
    if(flag == 1):
        dx *= -1
        player1_is_current = not player1_is_current
    elif(flag == -1):
        game_over()
        randomise_start()
        dx = abs(dx)
   
    pygame.display.update()