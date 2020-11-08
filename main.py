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
startmenu_screen = True
game_over_screen = False

# set last_update for time events
last_update = {}
last_update["game_start"] = pygame.time.get_ticks()

# store amount for respawn of villans
respawn = 0

# needed to spawn creatures at the beginning of the game
start_spawn = False
start_music = False

# main loop block
while running:
    # keep the loop running at the right speed
    GS.clock.tick(GS.FPS)

    # check if welcome screen should be displayed
    if startmenu_screen:
        GS.jukebox("menu")
        GS.startmenu()
        last_update["game_start"] = pygame.time.get_ticks()
        GS.jukebox("stop")
        start_spawn = True
        start_music = True
        startmenu_screen = False

    # wait for few seconds for villans to spawn and music to play
    # also good luck sound can ring through
    # and the player can be prepared for the enemys
    now = pygame.time.get_ticks()
    if not startmenu_screen \
            and start_music \
            and (now - last_update["game_start"]) > 1000:
        GS.jukebox("game")
        start_music = False

    if not startmenu_screen \
        and start_spawn \
        and (now - last_update["game_start"]) > 2000:
        respawn = 4
        start_spawn = False


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
    respawn = GS.generate_villans(respawn)


    # check sprite collisions
    respawn = GS.collision_check()


    # draw / render sprites
    GS.draw_everything()


    # after drawing, flip (CAF.GS).screen
    pygame.display.flip()
    pygame.display.update()
