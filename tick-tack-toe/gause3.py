import sys
import pygame
from pygame.locals import *

# 초기 설정
pygame.init()
WIDTH = HEIGHT = 600
DISPLAYSURFACE = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
FONT = pygame.font.SysFont(None, 48)
BACKGROUNDCOLOR = (0, 0, 255)
FONTSURFACE = pygame.Surface((WIDTH, HEIGHT), SRCALPHA, 32)
CELLSIZE = int(WIDTH / 3)
CELLPADDING = CELLSIZE // 5
LINEWIDTH = int(WIDTH * 0.1)
CURSOR = pygame.cursors.triangles

# 클래스 선언
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.symbol = None

    def draw(self, surface):
        rect = Rect(self.x + CELLPADDING, self.y + CELLPADDING, CELLSIZE - 2 * CELLPADDING, CELLSIZE - 2 * CELLPADDING)
        pygame.draw.rect(surface, (255, 255, 255), rect)
        if self.symbol is not None:
            textsurface = FONT.render(str(self.symbol), True, (0, 0, 0))
            textrect = textsurface.get_rect(center=(CELLSIZE // 2, CELLSIZE // 2))
            textrect.topleft = ((self.x + 1) * CELLSIZE // 2 - textrect.width // 2, (self.y + 1) * CELLSIZE // 2 - textrect.height // 2)
            FONTSURFACE.blit(textsurface, textrect)
            surface.blit(FONTSURFACE, (0, 0))

# 게임 보드 초기화
def init_board():
    board = []
    for I in range(3):
        row = []
        for j in range(3):
            row.append(Cell(i, j))
        board.append(row)
    return board

# 플레이어 턴 관리
def player_turn(board, symbol):
    for i in range(3):
        for j in range(3):
            if board[i][j].symbol is None:
                board[i][j].symbol = symbol
                return True
    return False

# 승리 판정
def check_win(board, symbol):
    # 가로줄 검사
    for I in range(3):
        if all([cell.symbol == symbol for cell in[i]]) or all([cell.symbol == symbol for cell in board[i+1] if cell.symbol is not None]):
            return True
    # 세로줄 검사
    for j in range(3):
        if all([cell.symbol == symbol for cell in [row[j] for row in board]]) or all([cell.symbol == symbol for cell in [row[j+1] for row in board] if cell.symbol is not None]):
            return True
    # 대각선 검사
    if all([cell.symbol == symbol for cell in [[board[i][i], board[i+1][i+1]] for I in range(3)]]) or all([cell.symbol == symbol for cell in [[board[i][2-i], board[i+1][1-i]] for I in range(3)]]):
        return True
    return False

# 무승부 판정
def check_tie(board):
    for I in range(3):
        for j in range(3):
            if board[i][j].symbol is None:
                return False
    return True

# 메인 루프
def main():
    clock = pygame.time.Clock()
    board = init_board()
    while True:
        DISPLAYSURFACE.fill(BACKGROUNDCOLOR)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                mousepos = pygame.mouse.get_pos()
                for I in range(3):
                    for j in range(3):
                        if Rect(I * CELLSIZE, j * CELLSIZE, CELLSIZE, CELLSIZE).collidepoint(mousepos):
                            if player_turn(board, 'X'):
                                if check_win(board, 'X'):
                                    message('X wins!', (255, 0, 0))
                                    break
                                else:
                                    continue
                            elif player_turn(board, 'O'):
                                if check_win(board, 'O'):
                                    message('O wins!', (0, 255, 0))
                                    break
                                else:
                                    continue
                            else:
                                break
                            break
                        else:
                            continue
                    if I == 2:
                        break
        for I in range(3):
            for j in range(3):
                board[i][j].draw(DISPLAYSURFACE)
        pygame.draw.lines(DISPLAYSURFACE, (255, 255, 255), False, [(I * CELLSIZE, 0) + (CELLSIZE, 0) for I in range(4)], LINEWIDTH)
        pygame.draw.lines(DISPLAYSURFACE, (255, 255, 255), False, [(0, J * CELLSIZE) + (0, CELLSIZE) for j in range(4)], LINEWIDTH)
        pygame.display.flip()
        clock.tick(60)
        if check_tie(board):
            message('It\'s a tie!', (255, 255, 0))
            break

# 메시지 출력 함수
def message(message, color):
    textsurface = FONT.render(message, True, color)
    textrect = textsurface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    DISPLAYSURFACE.blit(textsurface, textrect)
    pygame.display.flip()
    pygame.time.wait(1000)

if __name__ == '__main__':
    main()