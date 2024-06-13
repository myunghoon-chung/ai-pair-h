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
    cell_x = col * CELL_SIZE + CELL_SIZE // 2
    cell_y = row * CELL_SIZE + CELL_SIZE // 2
    cell_radius = CELL_SIZE // 2
    dist = ((mouse_pos[0] - cell_x)**2 + (mouse_pos[1] - cell_y)**2)**0.5
    return dist <= cell_radius

def switch_player(player):
    if player == PLAYER_ONE:
        return PLAYER_TWO
    else:
        return PLAYER_ONE

def is_winning(board, player):
    for row, col in product(range(3), repeat=3):
        if all(cell == player for cell in board[row]) or all(cell == player for cell in board[col]) or \
           (all(cell == player for cell in zip(*board)[row//2])) or \
           (all(cell == player for cell in zip(*board)[col//2])):
            return True
    return False

def show_winner_message(screen, player):
    font = pygame.font.SysFont('Arial', 50)
    message = f"{player} wins!"
    text = font.render(message, True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_rect().width // 2, SCREEN_HEIGHT // 2 - text.get_rect().height // 2))

def draw_board(screen, cell_size):
    for row in range(3):
        for col in range(3):
            rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, GREEN, rect)

def draw_board_state(screen, board, cell_size):
    for row in range(3):
        for col in range(3):
            text = board[row][col]
            text_surface = pygame.font.SysFont('Arial', int(cell_size * 0.7)).render(text, True, BLACK)
            text_rect = text_surface.get_rect(center=(col * cell_size + cell_size // 2, row * cell_size + cell_size // 2))
            screen.blit(text_surface, text_rect)
            
# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 플레이어가 클릭한 위치
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            selected_cell = (-1, -1)
            
            # 마우스 위치를 셀 위치로 변환
            for row in range(3):
                for col in range(3):
                    if mouse_in_cell(mouse_pos, row, col):
                        selected_cell = (row, col)
                        
            # 선택한 셀이 있고 빈 칸이면 게임 진행
            if selected_cell != (-1, -1) and board[selected_cell[0]][selected_cell[1]] == '-':
                current_player = switch_player(current_player)
                board[selected_cell[0]][selected_cell[1]] = current_player
                
                # 승리 여부 확인
                if is_winning(board, current_player):
                    show_winner_message(screen, current_player)
                    break
                    
    # 화면 그리기
    draw_board(screen, CELL_SIZE)
    draw_board_state(screen, board, CELL_SIZE)
    
    # 화면 갱신
    pygame.display.update()
    
# 종료
pygame.quit()