# library import block
import pygame
from game import *


# init block
pygame.init()


# game variable block
# set mainloop var
running = True

# for i in range(10):
#     i = GS.Meteor()
#     GS.all_sprites.add(i)
#     GS.meteors.add(i)

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

    # draw / render
    # GS.screen.fill(GS.BLACK)
    GS.screen.blit(GS.background_img, GS.background_img_rect)
    GS.all_sprites.draw(GS.screen)
    # pygame.draw.circle(GS.i.image, GS.RED, GS.i.rect.center, GS.i.radius)

    # after drawing, flip (CAF.GS).screen
    pygame.display.flip()
