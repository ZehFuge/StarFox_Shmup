# library import block
import pygame
from game import *
import random


# init block
pygame.init()


# game variable block
# set mainloop var
running = True

# set last_update for time events
last_update = pygame.time.get_ticks()

# enemy respawn variable for testing
respawn = 15

# main loop block
while running:
    # keep the loop running at the right speed
    GS.clock.tick(GS.FPS)

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
    # collision player by meteors
    hits = pygame.sprite.spritecollide(GS.player, GS.meteors, True, pygame.sprite.collide_circle)
    # player loses 1 life, also the hurt_mode is set to false to advoid the impact death
    if hits:
        GS.player.hurt()

    # if enemy dies through hit, raise respawn variable
    for hit in hits:
        respawn += 1


    # collision meteor by bullets
    hits = pygame.sprite.groupcollide(GS.meteors, GS.bullets, True, True)
    # if enemy dies through hit, raise respawn variable
    for hit in hits:
        GS.player.score += (100 - hit.radius) * GS.player.score_multiplier
        respawn += 1
        # 5% chance to drop power up by meteor kill
        if random.random() > 0.98:
            pow = GS.Power_Ups(hit.rect.center[0], hit.rect.center[1])
            GS.all_sprites.add(pow)
            GS.power_ups.add(pow)


    # enemy respawn loop
    if respawn > 0:
        i = GS.Meteor()
        GS.all_sprites.add(i)
        GS.meteors.add(i)
        respawn -= 1


    # collision player by power up
    hits = pygame.sprite.groupcollide(GS.power_ups, GS.players, True, False)
    for hit in hits:
        if hit.type == "wings":
            GS.player.power_level += 1
        if hit.type == "double":
            GS.player.score_multiplier *= 2


    # draw / render sprites
    # GS.screen.fill(GS.BLACK)
    GS.screen.blit(GS.background_img, GS.background_img_rect)
    GS.all_sprites.draw(GS.screen)

    # draw / render game interface
    # needs to be drawn last, to stay on top layer
    # draw_lives(surface, x, y, lives, img)
    GS.draw_lives(GS.screen, GS.WIDTH / 2, 5, GS.player.lives, GS.player_live_img)
    # draw the players hp bar
    GS.draw_shield_bar(GS.screen, GS.WIDTH - 210, 10, GS.player.shield)
    # draw score surface
    GS.draw_score()
    # draw the multiplier of the player
    GS.draw_multi()
    # draw_text(surface, text, size, x, y)


    # after drawing, flip (CAF.GS).screen
    pygame.display.flip()
    pygame.display.update()
