# pylint: disable=no-member, undefined-variable, invalid-syntax
# pylint: disable=no-member

import pygame, sys
from pygame.locals import*
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks()) - start_time
    score_surface = test_font.render(f'Score: {current_time}', False, 'Black')
    score_rect = score_surface.get_rect(center = (400, 50))
    screen.blit(score_surface,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            screen.blit(snail_surf,obstacle_rect)
        
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        
        return obstacle_list
    else: return[]

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def player_animation():
    # Usar la animación que camina si el jugador esta en el suelo
    # O usar la que brinca la superficie que brinca si no
    global player_surf, player_index #La variable global es una que sigue existiendo una vez se 
    #salga de la funcion

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1 #w1 = 0, w2 = 1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Surface Setting')
clock = pygame.time.Clock()
test_font = pygame.font.Font('Juego1/font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0

sky_surface = pygame.image.load('Juego1/graphics/Sky.png').convert()
ground_surface = pygame.image.load('Juego1/graphics/ground.png').convert()

#score_surf = test_font.render('My game', False, (64, 64, 64)).convert()
#score_rect = score_surf.get_rect(center = (400, 50))


#Obstacles
#Sanil
snail_frame1 = pygame.image.load('Juego1/graphics/snail/snail1.png').convert_alpha()
snail_frame2 = pygame.image.load('Juego1/graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame1, snail_frame2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

#Fly
fly_frame1 = pygame.image.load('Juego1/graphics/Fly/Fly1.png').convert_alpha()
fly_frame2 = pygame.image.load('Juego1/graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame1, fly_frame2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_list = []
obstacle_rect_list = []

player_walk_1 = pygame.image.load('Juego1/graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('Juego1/graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0 #Para escoger walk1 o walk2
player_jump = pygame.image.load('Juego1/graphics/Player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0

#Intro screen
player_stand = pygame.image.load('Juego1/graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400, 200))

game_name = test_font.render('Pixel Runner', False, (111,196,169))
game_name_rect=game_name.get_rect(center = (400, 80))

game_message = test_font.render('Press space tu run',False, (111,196,169))
game_message_rect = game_message.get_rect(center = (400, 340))

#Timer
obsticle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obsticle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #if event.type == pygame.MOUSEBUTTONUP:
            #print('mouse down')

        if game_active:    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos): 
                    player_gravity = -20
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    player_gravity = -20
        
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()
        
        if game_active:
            if event.type == obsticle_timer and game_active:
                if randint(0,2): #True=Snail, False=Fly
                    obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900, 1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900, 1100), 210)))
            
            if event.type == snail_animation_timer:
                if snail_frame_index == 0: snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]
            
            if event.type == fly_animation_timer:
                if fly_animation_timer == 0: fly_frame_index = 1
                else: fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index] 

    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        #pygame.draw.rect(screen, '#c0e8ec', score_rect)
        #pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
        #screen.blit(score_surf, score_rect)
        score = display_score()
    
        #snail_rect.x -= 4
        #if snail_rect.right <= 0: snail_rect.left = 800
        #screen.blit(snail_surf, snail_rect)

        #Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf, player_rect)

        #Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        
        #collision
        '''if snail_rect.colliderect(player_rect):
            game_active = False'''
        game_active = collisions(player_rect,obstacle_rect_list)
    
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear() #Para poder volver iniciar el juego bien otra vez
        #borra los osbstaculos que se quedaron cerca
        player_rect.midbottom = (80, 300) #Siempre reiniciara abajo
        player_gravity = 0 #Cuando se reinicie que no caiga más lejos

        score_message = test_font.render(f'Your score: {score}', False, (111, 196,169))
        score_message_rect = score_message.get_rect(center = (400,340))
        screen.blit(game_name, game_name_rect)
        
        if score == 0: screen.blit(game_message, game_message_rect)
        else: screen.blit(score_message, score_message_rect)
    

    pygame.display.update()
    clock.tick(60)
