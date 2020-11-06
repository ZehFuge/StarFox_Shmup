# library import block
import pygame
from game import *
import random


# init block
pygame.init()


# game variable block
# set mainloop var
running = True

# display welcome screen
welcome_screen = True
game_over_screen = False

# set last_update for time events
last_update = pygame.time.get_ticks()

# start the game with just 4 villans spawning
respawn = 4

# main loop block
while running:
    # keep the loop running at the right speed
    GS.clock.tick(GS.FPS)

    # check if welcome screen should be displayed
    if welcome_screen:
        GS.display_welcome()
        welcome_screen = False


    # check for closing game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GS.end_game()


    # check if player lost live and shall not be drawn
    if GS.player.hide:
        GS.all_sprites.remove(GS.player)
    if not GS.player.hide:
        GS.all_sprites.add(GS.player)


    # update / move sprites
    GS.all_sprites.update()


    # check if enemys need to be respawned
    # if respawn > 0:
    respawn = GS.generate_villans(respawn)


    # check sprite collisions
    respawn = GS.collision_check()


    # draw / render sprites
    GS.draw_everything()


    # after drawing, flip (CAF.GS).screen
    pygame.display.flip()
    pygame.display.update()
