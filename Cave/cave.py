import pygame
import random
import copy

pygame.init() 

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
large_font = pygame.font.SysFont(None, 72)
small_font = pygame.font.SysFont(None, 36)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 

airplane_image = pygame.image.load('airplane.png')
airplane_image = pygame.transform.scale(airplane_image, (60, 80))
airplane = airplane_image.get_rect(left=0, centery=SCREEN_HEIGHT // 2)

explosion_image = pygame.image.load('explosion.png')
explosion_image = pygame.transform.scale(explosion_image, (60, 60))
clock = pygame.time.Clock()

rects = [] 
for column_index in range(80):
    rect = pygame.Rect(column_index * 10, 100, 10, 400)
    rects.append(rect)


def runGame():
    score = 0
    game_over = False
    slope = 2
    airplane_dy = 2

    while True: 
        screen.fill(GREEN)

        event = pygame.event.poll() 
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                airplane_dy = -5 
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                airplane_dy = 5 

        score += 1

        new_rect = copy.deepcopy(rects[-1])
        test_rect = copy.deepcopy(rects[-1])
        test_rect.top = test_rect.top + slope
        if test_rect.top <= 0 or test_rect.bottom >= SCREEN_HEIGHT:
            slope = random.randint(2, 6) * (-1 if slope > 0 else 1) 
            new_rect.height = new_rect.height + -20 
        new_rect.left = new_rect.left + 10
        new_rect.top = new_rect.top + slope
        rects.append(new_rect)
        for rect in rects:
            rect.left = rect.left - 10
        del rects[0]

        airplane.top += airplane_dy 

        if airplane.top < rects[0].top or airplane.bottom > rects[0].bottom:
            game_over = True

        for rect in rects:
            pygame.draw.rect(screen, BLACK, rect)

        screen.blit(airplane_image, airplane)

        score_image = small_font.render('Point {}'.format(score), True, YELLOW)
        screen.blit(score_image, (10, 10))

        if game_over == True:
            screen.blit(explosion_image, (0, airplane.top - 40))

            game_over_image = large_font.render('Game over', True, RED)
            screen.blit(game_over_image, game_over_image.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2))

        pygame.display.update() 
        clock.tick(30) 

runGame()
pygame.quit()
