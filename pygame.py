import pygame
import random

pygame.init()

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetris')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLOR_LIST = [(0, 255, 255), (0, 0, 255), (255, 165, 0), (255, 0, 0), (0, 255, 0), (255, 255, 0), (128, 0, 128)]

BLOCK_SIZE = 30
COLUMN_COUNT = SCREEN_WIDTH // BLOCK_SIZE
ROW_COUNT = SCREEN_HEIGHT // BLOCK_SIZE

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[0, 1, 0], [1, 1, 1]]
]

# Load background image
background_image = pygame.image.load('NAROTORIBUUT.jpeg')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale the image to fit the screen
background_rect = background_image.get_rect()

# Load music
pygame.mixer.music.load('Tetris_Theme_Piano_Version_-_400k_Special_[_YTBMP3.org_].mp3')  # Load the background music file
pygame.mixer.music.set_volume(0.5)  # Set volume level (0.0 to 1.0)
pygame.mixer.music.play(-1, 0.0)  # Play music in loop (-1 means infinite loop)

def draw_grid():
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        pygame.draw.line(SCREEN, WHITE, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
        pygame.draw.line(SCREEN, WHITE, (0, y), (SCREEN_WIDTH, y))

def draw_shape(shape, offset, color):
    shape_height = len(shape)
    shape_width = len(shape[0])
    for y in range(shape_height):
        for x in range(shape_width):
            if shape[y][x] == 1:
                pygame.draw.rect(SCREEN, color, ((offset[0] + x) * BLOCK_SIZE, (offset[1] + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def valid_move(board, shape, offset):
    shape_height = len(shape)
    shape_width = len(shape[0])
    for y in range(shape_height):
        for x in range(shape_width):
            if shape[y][x] == 1:
                new_x = offset[0] + x
                new_y = offset[1] + y
                if new_x < 0 or new_x >= COLUMN_COUNT or new_y >= ROW_COUNT or board[new_y][new_x] != 0:
                    return False
    return True

def clear_lines(board):
    full_lines = [i for i, row in enumerate(board) if all(col != 0 for col in row)]
    for i in full_lines:
        board.pop(i)
        board.insert(0, [0] * COLUMN_COUNT)
    return len(full_lines)

def run_game():
    clock = pygame.time.Clock()
    board = [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]
    current_shape = random.choice(SHAPES)
    current_color = random.choice(COLOR_LIST)
    offset = [COLUMN_COUNT // 2 - len(current_shape[0]) // 2, 0]
    score = 0

    game_over = False

    while not game_over:
        SCREEN.fill(BLACK)
        SCREEN.blit(background_image, background_rect)  # Draw the background image
        draw_grid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if valid_move(board, current_shape, [offset[0] - 1, offset[1]]):
                offset[0] -= 1
        if keys[pygame.K_RIGHT]:
            if valid_move(board, current_shape, [offset[0] + 1, offset[1]]):
                offset[0] += 1
        if keys[pygame.K_DOWN]:
            if valid_move(board, current_shape, [offset[0], offset[1] + 1]):
                offset[1] += 1
        if keys[pygame.K_UP]:
            rotated_shape = [list(row) for row in zip(*current_shape[::-1])]
            if valid_move(board, rotated_shape, offset):
                current_shape = rotated_shape

        if not valid_move(board, current_shape, [offset[0], offset[1] + 1]):
            for y in range(len(current_shape)):
                for x in range(len(current_shape[0])):
                    if current_shape[y][x] == 1:
                        board[offset[1] + y][offset[0] + x] = COLOR_LIST.index(current_color) + 1
            score += clear_lines(board)
            current_shape = random.choice(SHAPES)
            current_color = random.choice(COLOR_LIST)
            offset = [COLUMN_COUNT // 2 - len(current_shape[0]) // 2, 0]
            if not valid_move(board, current_shape, offset):
                game_over = True

        draw_shape(current_shape, offset, current_color)
        for y, row in enumerate(board):
            for x, cell in enumerate(row):
                if cell != 0:
                    pygame.draw.rect(SCREEN, COLOR_LIST[cell - 1], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    run_game()
