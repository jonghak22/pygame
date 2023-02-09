import pygame 
import random

pygame.init() 

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
large_font = pygame.font.SysFont(None, 72)
small_font = pygame.font.SysFont(None, 36)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

CELL_SIZE = 50
COLUMN_COUNT = SCREEN_WIDTH // CELL_SIZE
ROW_COUNT = SCREEN_HEIGHT // CELL_SIZE

grid = [[{'mine': False, 'open': False, 'mine_count_around': 0, 'flag': False} for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]
MINE_COUNT = 15
for _ in range(MINE_COUNT):
    while True:
        column_index = random.randint(0, COLUMN_COUNT - 1)
        row_index = random.randint(0, ROW_COUNT - 1)
        tile = grid[row_index][column_index]
        if not tile['mine']:
            tile['mine'] = True 
            break

clock = pygame.time.Clock() 

def in_bound(column_index, row_index):
    if (0 <= column_index < COLUMN_COUNT and 0 <= row_index < ROW_COUNT):
        return True
    else:
        return False

def open_tile(column_index, row_index): 
    if not in_bound(column_index, row_index):
        return

    tile = grid[row_index][column_index]
    if not tile['open']:
        tile['open'] = True
    else:    
        return

    if tile['mine']:
        return

    mine_count_around = get_mine_count_around(column_index, row_index)
    if mine_count_around > 0:
        tile['mine_count_around'] = mine_count_around
    else:
        for dc, dr in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            column_index_around, row_index_around = (column_index + dc, row_index + dr)
            open_tile(column_index_around, row_index_around)

def get_mine_count_around(column_index, row_index):
    count = 0

    for dc, dr in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
        column_index_around, row_index_around = (column_index + dc, row_index + dr)
        if in_bound(column_index_around, row_index_around) and grid[row_index_around][column_index_around]['mine']:
            count += 1
    return count

def runGame():
    SUCCESS = 1
    FAILURE = 2
    game_over = 0

    while True: 
        clock.tick(30) 
        screen.fill(BLACK) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                column_index = event.pos[0] // CELL_SIZE
                row_index = event.pos[1] // CELL_SIZE
                if event.button == 1:
                    if in_bound(column_index, row_index):
                        tile = grid[row_index][column_index]
                        if tile['mine']:
                            tile['open'] = True
                            game_over = FAILURE
                        else:
                            open_tile(column_index, row_index)
                elif event.button == 3:
                    if in_bound(column_index, row_index):
                        tile = grid[row_index][column_index]
                        if not tile['flag']:
                            tile['flag'] = True
                        else:
                            tile['flag'] = False

                        success = True
                        for row_index in range(ROW_COUNT):
                            for column_index in range(COLUMN_COUNT):
                                tile = grid[row_index][column_index]
                                if tile['mine'] and not tile['flag']:
                                    success = False
                                    break
                        if success:
                            game_over = SUCCESS

        for column_index in range(COLUMN_COUNT):
            for row_index in range(ROW_COUNT):
                tile = grid[row_index][column_index]
                if tile['mine_count_around']:
                    mine_count_around_image = small_font.render('{}'.format(tile['mine_count_around']), True, YELLOW)
                    screen.blit(mine_count_around_image, mine_count_around_image.get_rect(centerx=column_index * CELL_SIZE + CELL_SIZE // 2, centery=row_index * CELL_SIZE + CELL_SIZE // 2))
                if tile['mine']: 
                    mine_image = small_font.render('x', True, RED)
                    screen.blit(mine_image, mine_image.get_rect(centerx=column_index * CELL_SIZE + CELL_SIZE // 2, centery=row_index * CELL_SIZE + CELL_SIZE // 2)) #지뢰 설치
                if not tile['open']:
                    pygame.draw.rect(screen, GRAY, pygame.Rect(column_index * CELL_SIZE, row_index * CELL_SIZE, CELL_SIZE, CELL_SIZE)) #커버
                if tile['flag']: 
                    v_image = small_font.render('v', True, WHITE)
                    screen.blit(v_image, (column_index * CELL_SIZE + 10, row_index * CELL_SIZE + 10)) 
                pygame.draw.rect(screen, WHITE, pygame.Rect(column_index * CELL_SIZE, row_index * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

        if game_over > 0:
            if game_over == SUCCESS:
                success_image = large_font.render('Success', True, RED)
                screen.blit(success_image, success_image.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2))
            elif game_over == FAILURE:
                failure_image = large_font.render('Failure', True, RED)
                screen.blit(failure_image, failure_image.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2))

        pygame.display.update() 

runGame()
pygame.quit() 