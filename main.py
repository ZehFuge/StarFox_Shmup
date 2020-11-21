# library import block
import pygame
from game import *


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


# store amount for respawn of villans
respawn = 0
allow_respawn = True


# needed to spawn creatures at the beginning of the game
start_spawn = False
killed_spawn = False
start_music = False


# main loop block
while running:
    # keep the loop running at the right speed
    GS.clock.tick(GS.FPS)

    # check if player died
    if GS.player.lives == 0:
        # play gameover sound
        GS.voice_sound["player_death"].play()
        startmenu_screen = GS.display_game_over()

        # if player didnt closed the game
        respawn = GS.reset_game()
        last_update["game_start"] = pygame.time.get_ticks()
        start_music = True
        start_spawn = True


    # check if welcome screen should be displayed
    if startmenu_screen:
        GS.jukebox("menu")
        GS.start_menu()
        last_update["game_start"] = pygame.time.get_ticks()
        GS.jukebox("stop")
        start_spawn = True
        start_music = True
        startmenu_screen = False

    # destroy all sprites, if player got killed and save their amount
    # also forbid enemy spawning
    # killed_spawn allows the statement to be executed only once
    if not GS.player.hurt_mode \
        and not killed_spawn:
        # save the amount of from screen cleared villans
        respawn = GS.killer.kill_and_count()

        # check if respawn amount is to overwhelming for the player
        if respawn >= 20:
            respawn = 10

        # save the time of the player death
        last_update["got_killed"] = pygame.time.get_ticks()

        # change killed_spawn to denied second execute of this if statement
        killed_spawn = True

        # forbid enemy spawning
        allow_respawn = False

    now = pygame.time.get_ticks()
    # allow to spawn villans again
    # 1 second after player recovered from lifeloss
    if GS.player.hurt_mode \
            and killed_spawn \
            and (now - last_update["got_killed"]) >= (GS.player.hurt_delay + 1000):
        # 1 second after player spawn, change killed spawn to be able to execute again, if player dies again
        killed_spawn = False

        # allow enemy spawning
        allow_respawn = True

    # wait few seconds for villans to spawn and music to play
    # also good luck sound can ring through
    # and the player can be prepared for the enemys
    now = pygame.time.get_ticks()
    if not startmenu_screen \
            and start_music \
            and (now - last_update["game_start"]) > 1000:
        GS.jukebox("game")
        start_music = False

    # allow enemy spawning 3 seconds after game start
    if not startmenu_screen \
        and start_spawn \
        and (now - last_update["game_start"]) > 3000:
        respawn = 4
        start_spawn = False


    # check for closing game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GS.end_game()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                wasted_time = GS.pause_menu()
                # correct time events
                GS.more_villans += wasted_time


    # update / move sprites
    GS.all_sprites.update()


    # check if enemys need to be respawned
    if allow_respawn:
        respawn = GS.generate_villans(respawn)


    # check sprite collisions
    if allow_respawn:
     respawn = GS.collision_check()


    # draw / render sprites
    GS.draw_everything()


    # after drawing, flip screen
    pygame.display.flip()
