import pygame
from itertools import product

# 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# 셀 크기
CELL_SIZE = SCREEN_WIDTH // 3

# 플레이어 순서
PLAYER_ONE = 'X'
PLAYER_TWO = 'O'
current_player = PLAYER_ONE

# 보드 상태
board = [['-' for _ in range(3)] for __ in range(3)]

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def mouse_in_cell(mouse_pos, row, col):
    cell_x = col * CELL_SIZE
    cell_y = row * CELL_SIZE
    cell_rect = pygame.Rect(cell_x, cell_y, CELL_SIZE, CELL_SIZE)
    return cell_rect.collidepoint(mouse_pos)

def switch_player(player):
    return PLAYER_TWO if player == PLAYER_ONE else PLAYER_ONE

def is_winning(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def show_winner_message(screen, player):
    font = pygame.font.SysFont('Arial', 50)
    message = f"{player} wins!"
    text = font.render(message, True, WHITE)
    screen.fill(BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_rect().width // 2, SCREEN_HEIGHT // 2 - text.get_rect().height // 2))
    pygame.display.update()
    pygame.time.wait(2000)

def draw_board(screen, cell_size):
    screen.fill(WHITE)
    for row in range(3):
        for col in range(3):
            rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, GREEN, rect, 3)

def draw_board_state(screen, board, cell_size):
    for row in range(3):
        for col in range(3):
            text = board[row][col]
            if text != '-':
                text_surface = pygame.font.SysFont('Arial', int(cell_size * 0.7)).render(text, True, BLACK)
                text_rect = text_surface.get_rect(center=(col * cell_size + cell_size // 2, row * cell_size + cell_size // 2))
                screen.blit(text_surface, text_rect)

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for row in range(3):
                for col in range(3):
                    if mouse_in_cell(mouse_pos, row, col):
                        if board[row][col] == '-':
                            board[row][col] = current_player
                            if is_winning(board, current_player):
                                show_winner_message(screen, current_player)
                                running = False
                            current_player = switch_player(current_player)
                            break

    draw_board(screen, CELL_SIZE)
    draw_board_state(screen, board, CELL_SIZE)
    pygame.display.update()

pygame.quit()
