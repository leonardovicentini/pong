#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Leonardo Vicentini"
__version__ = "01_01"


import sys
import pygame
import random


boold = False


if __name__ == "__main__":

    if boold:
        print("Start main")

    # Initializing pygame and the screen
    pygame.init()
    colore = 255, 255, 255
    sfondo = 0, 0, 0
    w_width, w_height = 800, 500
    win = pygame.display.set_mode((w_width, w_height))
    pygame.display.set_caption("Pong")
    font_score = pygame.font.SysFont("comicsans", int(w_height * 0.15), True)
    font_title = pygame.font.SysFont("comicsans", 100, True)
    font_subtitle = pygame.font.SysFont("comicsans", 25, True)
    score_sound = pygame.mixer.Sound("../sounds/score.wav")
    catch_sound = pygame.mixer.Sound("../sounds/catch.wav")
    
    # Initializing the game variables
    r_width, r_height = int(w_width / 64), int(w_height / 9)
    x_p1, y_p1 = int(w_height / 8), int(w_height / 2)
    x_p2, y_p2 = w_width - (int(w_height / 8) + r_width), int(w_height / 2)
    x_b, y_b = int(w_width / 2), int(w_height / 2)
    ball_radius = int(w_height / 88)
    
    score_value_p1 = 0
    score_value_p2 = 0

    player_speed = 50
    ball_speed_x = 25
    ball_speed_y = 0

    run = False

    if boold: print("Starting menu...")
    # Starting menu
    while not run:
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_s]:
            if boold: print("Avvio del gioco...")
            run = True

        title = font_title.render("Pong", 1, colore)
        start_intructions = font_subtitle.render("Press 's' to start", 1, colore)
        players = font_subtitle.render("Player 1                    Player2", 1, colore)
        up_commands = font_subtitle.render("        'w'                       'UP_ARROW'", 1, colore)
        down_commands = font_subtitle.render("            's'                      'DOWN_ARROW'", 1, colore)

        win.fill(sfondo)
        win.blit(title, ((w_width - title.get_rect().width)/2, 50))
        win.blit(players, ((w_width - players.get_rect().width)/2, 175))
        win.blit(up_commands, ((w_width - up_commands.get_rect().width)/2, 225))
        win.blit(down_commands, ((w_width - down_commands.get_rect().width)/2, 275))
        win.blit(start_intructions, ((w_width - start_intructions.get_rect().width)/2, 400))
        pygame.display.update() 
        pygame.time.delay(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    # game lifecycle
    while run:
        
        # scorekeeper
        score_p1 = font_score.render(f"{score_value_p1}", 1, colore)
        score_p2 = font_score.render(f"{score_value_p2}", 1, colore)

        # reading input
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and y_p1 > 0:
            y_p1 -= player_speed

        if keys[pygame.K_s] and y_p1 < (w_height - r_height):
            y_p1 += player_speed
        
        if keys[pygame.K_UP] and y_p2 > 0:
            y_p2 -= player_speed
        
        if keys[pygame.K_DOWN] and y_p2 < (w_height - r_height):
            y_p2 += player_speed

        if boold:
            print(f"position player 1: x={x_p1} y={y_p1}\tposition player 2: X={x_p2} y={y_p2}\tposition ball: x={x_b} y={y_b}\tvelocita y della palla: {ball_speed_y}")
        
        # ball movements
        # bounce on high walls
        if y_b + ball_radius >= w_height or y_b - ball_radius < 0:
           ball_speed_y = - ball_speed_y
           catch_sound.play()

        # bounce on players
        if (x_b - ball_radius in range(x_p1, x_p1 + r_width) and y_b in range(y_p1 - 50, y_p1 + r_height + 50)) or \
           (x_b + ball_radius in range(x_p2, x_p2 + r_width) and y_b in range(y_p2 - 50, y_p2 + r_height + 50)):
            # ball bounce
            ball_speed_x = - ball_speed_x
            # change the angle of the ball
            ball_speed_y = random.randrange(-41, 41)
            catch_sound.play()

        x_b += ball_speed_x
        y_b += ball_speed_y


        # Point assignment
        if x_b < x_p1 - 100:
            score_value_p2 += 1
            x_b, y_b = int(w_width / 2), int(w_height / 2)
            ball_speed_y = 0
            ball_speed_x = ball_speed_x if random.randrange(0, 2) else - ball_speed_x
            score_sound.play()
            pygame.time.delay(750)

        if x_b > x_p2 + 100:
            score_value_p1 += 1
            x_b, y_b = int(w_width / 2), int(w_height / 2)
            ball_speed_y = 0
            ball_speed_x = ball_speed_x if random.randrange(0, 2) else - ball_speed_x
            score_sound.play()
            pygame.time.delay(750)
            
        # I drawing all the objects
        win.fill(sfondo) 
        pygame.draw.rect(win, colore, (x_p1, y_p1, r_width, r_height)) 
        pygame.draw.rect(win, colore, (x_p2, y_p2, r_width, r_height))
        pygame.draw.rect(win, colore, (w_width / 2 - 2, 0, 4, 1000))
        pygame.draw.circle(win, colore, (x_b, y_b), ball_radius)
        win.blit(score_p1, (w_width / 4, 40))
        win.blit(score_p2, (w_width - (w_width/4 + score_p2.get_rect().width), 40))
    
        pygame.display.update() 
        pygame.time.delay(35)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if boold: print("Showing final results...")
                final_title = font_title.render("Final score", 1, colore)
                p1_final_score = font_score.render(f"Player 1:     {score_value_p1}", 1, colore)
                p2_final_score = font_score.render(f"Player 2:     {score_value_p2}", 1, colore)
                win.fill(sfondo)
                win.blit(final_title, ((w_width - final_title.get_rect().width)/2, 50))
                win.blit(p1_final_score, ((w_width - p1_final_score.get_rect().width)/2, 250))
                win.blit(p2_final_score, ((w_width - p2_final_score.get_rect().width)/2, 350))
                pygame.display.update()
                pygame.time.delay(2000) 
                run = False

    pygame.quit()

    if boold:
        print("End main")
