import pygame

pygame.init()

WHITE = (255,255,255)
BLACK = (0, 0, 0)
screen_width=400
screen_height=300
screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()


def runGame():
    bar_width, bar_height = screen_width / 32., screen_height / 6.
    bar_dist_from_edge = screen_width / 64.
    bar_1_start_x = bar_dist_from_edge
    bar_start_y = (screen_height - bar_height) / 2.
    bar_max_y = screen_height - bar_height - bar_dist_from_edge

    circle_diameter = screen_height / 16.
    circle_radius = circle_diameter / 2.
    circle_start_x, circle_start_y = (screen_width - circle_diameter), (screen_width - circle_diameter) / 2.

    bar = pygame.Surface((int(bar_width), int(bar_height)))
    bar1 = bar.convert()
    bar1.fill(WHITE)

    circle_surface = pygame.Surface((int(circle_diameter), int(circle_diameter)))
    pygame.draw.circle(circle_surface, WHITE, (int(circle_radius), int(circle_radius)), int(circle_radius))
    circle = circle_surface.convert()

    bar1_x = bar_1_start_x
    bar1_y = bar_start_y
    circle_x, circle_y = circle_start_x, circle_start_y
    bar1_move = 0
    speed_x, speed_y, speed_bar = -screen_width / 1.28, screen_height / 1.92, screen_height * 1.2

    while True:
        time_passed = clock.tick(30)
        time_sec = time_passed / 1000.0
        screen.fill(BLACK)

        circle_x += speed_x * time_sec
        circle_y += speed_y * time_sec
        ai_speed = speed_bar * time_sec

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    bar1_move = -ai_speed
                elif event.key == pygame.K_DOWN:
                    bar1_move = ai_speed
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    bar1_move = 0
                elif event.key == pygame.K_DOWN:
                    bar1_move = 0
        
        bar1_y += bar1_move
    
        if bar1_y >= bar_max_y:
            bar1_y = bar_max_y
        elif bar1_y <= bar_dist_from_edge:
            bar1_y = bar_dist_from_edge

        if circle_x < bar_dist_from_edge + bar_width:
            if circle_y >= bar1_y - circle_radius and circle_y <= bar1_y + bar_height + circle_radius:
                circle_x = bar_dist_from_edge + bar_width
                speed_x = -speed_x
        if circle_x < -circle_radius:
            circle_x, circle_y = circle_start_x, circle_start_y
            bar1_y, bar_2_y = bar_start_y, bar_start_y
        elif circle_x > screen_width - circle_diameter:
            speed_x = -speed_x
        if circle_y <= bar_dist_from_edge:
            speed_y = -speed_y
            circle_y = bar_dist_from_edge
        elif circle_y >= screen_height - circle_diameter - circle_radius:
            speed_y = -speed_y
            circle_y = screen_height - circle_diameter - circle_radius

        screen.blit(bar1, (bar1_x, bar1_y))
        screen.blit(circle, (circle_x, circle_y))
        pygame.display.update()

runGame()
pygame.quit()
