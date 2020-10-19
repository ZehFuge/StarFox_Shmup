# library import block
import pygame
from game import *


# init block
pygame.init()


# game variable block
# set mainloop var
running = True


# enemy respawn variable for testing
respawn = 10

# main loop block
while running:
    # keep the loop running at the right speed
    GS.clock.tick(GS.FPS)

    # check for closing game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GS.end_game()

    # update sprites
    GS.all_sprites.update()


    # check sprite collision
    # collision player by meteors
    hits = pygame.sprite.spritecollide(GS.player, GS.meteors, True, pygame.sprite.collide_circle)
    # if enemy dies through hit, raise respawn variable
    for hit in hits:
        respawn += 1

    # collision meteor by bullets
    hits = pygame.sprite.groupcollide(GS.meteors, GS.bullets, True, True)
    # if enemy dies through hit, raise respawn variable
    for hit in hits:
        respawn += 1


    # enemy respawn loop
    if respawn > 0:
        i = GS.Meteor()
        GS.all_sprites.add(i)
        GS.meteors.add(i)
        respawn -= 1


    # draw / render sprites
    # GS.screen.fill(GS.BLACK)
    GS.screen.blit(GS.background_img, GS.background_img_rect)
    GS.all_sprites.draw(GS.screen)

    # draw / render game interface
    # needs to be drawn last, to stay on top layer
    # draw_lives(surface, x, y, lives, img)
    GS.draw_lives(GS.screen, GS.WIDTH - 100, 5, GS.player.lives, GS.player_live_img)
    # draw_text(surface, text, size, x, y)


    # after drawing, flip (CAF.GS).screen
    pygame.display.flip()
