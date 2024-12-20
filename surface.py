# pylint: disable=no-member, undefined-variable, invalid-syntax
# pylint: disable=no-member

import pygame, sys
from pygame.locals import*

pygame.init()
screen = pygame.display.set_mode((600, 360))
pygame.display.set_caption('Surface Setting')
clock = pygame.time.Clock()
test_font = pygame.font.Font('comicsans', 50)

cats_surface = pygame.image.load('Tut/cats.png')
cats2_surface = pygame.image.load('Tut/cats2.png')
text_surface = test_font.render('My game', False, 'Black')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(cats_surface, (0,0))
    screen.blit(cats2_surface, (40,220))
    screen.blit(text_surface, (300, 50))

    pygame.display.update()
    clock.tick(60)
