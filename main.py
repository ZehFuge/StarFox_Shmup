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

# enemy respawn variable for testing
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


    # check sprite collisions
    # player hit by others
    # collision player by meteors
    hits = pygame.sprite.spritecollide(GS.player, GS.meteors, True, pygame.sprite.collide_circle)
    # player loses 1 life, also the hurt_mode is set to false to advoid the impact death
    for hit in hits:
        # create explosion image
        explosion = GS.Explosion(hit.rect.center, "lg")
        GS.all_sprites.add(explosion)

        # hurt the player
        GS.player.hurt()
    # if meteor dies through hit, raise respawn variable
    for hit in hits:
        respawn += 1


    # collision player by enemy
    hits = pygame.sprite.spritecollide(GS.player, GS.enemys, True, pygame.sprite.collide_circle)
    # player loses 1 life, also the hurt_mode is set to false to advoid the impact death
    for hit in hits:
        # create explosion image
        explosion = GS.Explosion(hit.rect.center, "lg")
        GS.all_sprites.add(explosion)

        # hurt the player
        GS.player.hurt()
    # if enemy dies through hit, raise respawn variable
    for hit in hits:
        respawn += 1


    # collision player by enemy_bullets
    hits = pygame.sprite.spritecollide(GS.player, GS.enemy_bullets, True)
    # remove player HP if hit
    for hit in hits:
        # create explosion image
        explosion = GS.Explosion(hit.rect.center, "sm")
        GS.all_sprites.add(explosion)

        # hurt the player
        GS.player.hurt()


    # collision meteor by bullets
    hits = pygame.sprite.groupcollide(GS.meteors, GS.bullets, True, True)
    # if meteor dies through hit, raise respawn variable
    for hit in hits:
        # create explosion image and play its sound
        explosion = GS.Explosion(hit.rect.center, "lg")
        GS.all_sprites.add(explosion)
        GS.explosion_sound.play()

        # calculate new player score
        GS.player.score += (100 - hit.radius) * GS.player.score_multiplier
        respawn += 1
        # 5% chance to drop power up by meteor kill
        if random.random() >= 0.95:
            pow = GS.Power_Ups(hit.rect.center[0], hit.rect.center[1])
            GS.all_sprites.add(pow)
            GS.power_ups.add(pow)


    # collision enemys by bullets
    hits = pygame.sprite.groupcollide(GS.enemys, GS.bullets, True, True)
    # if enemy dies through hit, raise respawn variable
    for hit in hits:
        # create explosion image and play its sound
        explosion = GS.Explosion(hit.rect.center, "lg")
        GS.all_sprites.add(explosion)
        GS.explosion_sound.play()

        # calculate new player score
        GS.player.score += 100 * GS.player.score_multiplier
        respawn += 1
        # 5% chance to drop power up by enemy kill
        if random.random() > 0.95:
            pow = GS.Power_Ups(hit.rect.center[0], hit.rect.center[1])
            GS.all_sprites.add(pow)
            GS.power_ups.add(pow)

    # check if enemys need to be respawned
    if respawn > 0:
        respawn = GS.generate_villans(respawn)


    # collision player by power up
    hits = pygame.sprite.groupcollide(GS.power_ups, GS.players, True, False)
    for hit in hits:
        # enhence the quantity of players lasers
        if hit.type == "wings":
            GS.power_up_sound["wings"].play()
            GS.player.power_level += 1
        # raise the multiplicator score of the player
        if hit.type == "double":
            GS.power_up_sound["double"].play()
            GS.player.score_multiplier += 1
        # heal player for a little bit
        if hit.type == "silver":
            GS.power_up_sound["rings"].play()
            GS.player.shield += 15
            # check if players life raised above 100 and correct it
            if GS.player.shield > 100:
                GS.player.shield = 100
        # heal player for a big amount
        if hit.type == "gold":
            GS.power_up_sound["rings"].play()
            GS.player.shield += 50
            # check if players life raised above 100 and correct it
            if GS.player.shield > 100:
                GS.player.shield = 100


    # draw / render sprites
    GS.draw_the_rest()


    # after drawing, flip (CAF.GS).screen
    pygame.display.flip()
    pygame.display.update()
