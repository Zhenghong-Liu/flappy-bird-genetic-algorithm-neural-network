import sys

import pygame
import random
import numpy as np
from pygame.locals import *

# Game constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.5
FLAP_STRENGTH = 10
OBSTACLE_SPEED = 5
OBSTACLE_GAP = 150

MUTATION_RATE = 1

#colors
BG_COLOR = (255,255, 255)
BIRD_COLOR = (0,0,0)
PILLAR_COLOR = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)


class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.vel_y = 0
        self.height = 26
        self.width = 26

    def flap(self):
        self.vel_y = -FLAP_STRENGTH

    def update(self):
        self.vel_y += GRAVITY
        self.y += self.vel_y


class Pillar:
    def __init__(self, x):
        gap_y = random.randint(100, 300)
        self.width = 80
        self.top = pygame.Rect(x, 0, self.width, gap_y - OBSTACLE_GAP // 2)
        self.bottom = pygame.Rect(x, gap_y + OBSTACLE_GAP // 2, self.width, SCREEN_HEIGHT - gap_y - OBSTACLE_GAP // 2)


    def update(self):
        self.top.x -= OBSTACLE_SPEED
        self.bottom.x -= OBSTACLE_SPEED



def hit(bird, pillar):

    if bird.y - bird.height//2 <=0 or bird.y + bird.height//2 >= SCREEN_HEIGHT:
        return True

    if bird.x + bird.width//2 >= pillar.top.x and bird.x - bird.width//2 <= pillar.top.x + pillar.top.width:
        if bird.y - bird.height//2 <= pillar.top.y + pillar.top.height or bird.y + bird.height//2 >= pillar.bottom.y:

            return True
    return False

def update_score(bird,pillar,score,through_flag,through_flag_last):
    if bird.x + bird.width//2 >= pillar.top.x and bird.x - bird.width//2 <= pillar.top.x + pillar.top.width:
        through_flag = True
    else:
        through_flag = False

    if through_flag_last == True and through_flag == False:
        score += 1
    through_flag_last = through_flag
    return score,through_flag,through_flag_last

def manual_game():
    bird = Bird()
    pillars = [Pillar(400)]

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    score = 0
    through_flag = False
    through_flag_last = False
    score_font = pygame.font.Font('arial.ttf', 32)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                bird.flap()

            if event.type == KEYDOWN:
                bird.flap()

        screen.fill(BG_COLOR)

        # Draw bird
        pygame.draw.circle(screen, RED, (bird.x, bird.y), bird.width)

        # Update bird
        bird.update()

        # Draw pillars
        for pillar in pillars:
            pygame.draw.rect(screen, GREEN, pillar.top)
            pygame.draw.rect(screen, GREEN, pillar.bottom)

        #draw score
        score_text = score_font.render(str(score),True,RED)
        screen.blit(score_text,(10,10))


        # Update pillars
        pillars[0].update()
        if pillars[0].top.x < -pillars[0].width:
            pillars.pop(0)
            pillars.append(Pillar(400))

        # Check for hits
        if hit(bird, pillars[0]):
            print("Game over!")
            print("Final score:",score)
            break

        score,through_flag,through_flag_last = update_score(bird,pillars[0],score,through_flag,through_flag_last)

        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    manual_game()
