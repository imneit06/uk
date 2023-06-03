import pygame, sys, random
pygame.init()

def draw_floor():
    screen.blit(floor,(floor_x_pos,600))
    screen.blit(floor,(floor_x_pos+432,600))
def create_pipe():
    pipe_random_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (500,pipe_random_pos))
    top_pipe = pipe_surface.get_rect(midtop = (500,pipe_random_pos-650))
    return bottom_pipe, top_pipe
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 1.5
    return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 700: 
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe, pipe)
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >=600:
        return False
    return True  
def rotate_bird(bird1):
    new_bird =  pygame.transform.rotozoom(bird1, -bird_movement*3,1)
    return new_bird
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect
def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'score: {int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,50))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'high score: {int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (216,100))
        screen.blit(high_score_surface,high_score_rect)
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

screen = pygame.display.set_mode((432,700))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',40)


gravity = 0.17
bird_movement = 0
game_active = True
score = 0
high_score = 0


background = pygame.image.load('assets/background-night.png').convert()
background = pygame.transform.scale2x(background)
floor = pygame.image.load('assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

bird_down = pygame.image.load('assets/yellowbird-downflap.png').convert_alpha()
bird_mid = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
bird_up = pygame.image.load('assets/yellowbird-upflap.png').convert_alpha()
bird_list = [bird_down,bird_mid,bird_up]
bird_index = 0
bird = bird_list[bird_index]
#bird = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
#bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center = (100, 350))
bird_flap = pygame.USEREVENT+1
pygame.time.set_timer(bird_flap,300)


pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe,1800)
pipe_height = [250,300,350,400]

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_surface_rect = game_over_surface.get_rect(center = (216,350))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement = -4
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,350)
                bird_movement = 0
                score = 0
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())  #return 1 cai -> append 2 cai -> extend
        if event.type == bird_flap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
        bird, bird_rect = bird_animation()


    screen.blit(background,(0,0)) 


    if game_active:
        rotated_bird = rotate_bird(bird)
        screen.blit(rotated_bird, bird_rect)
        bird_movement += gravity
        bird_rect.centery += bird_movement

        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        
        
        game_active = check_collision(pipe_list)

        score += 0.1
        score_display('main_game')
    else:
        high_score = update_score(score,high_score)
        score_display('game_over')
        screen.blit(game_over_surface,game_over_surface_rect)
    floor_x_pos-=1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0

  


    pygame.display.update()
    clock.tick(120)
