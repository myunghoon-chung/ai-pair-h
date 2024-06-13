import sys
import pygame
from pygame.locals import *

# 게임판을 그리는 함수
def draw_board(board, screen):
    screen.fill((255, 255, 255))
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell == 'X':
                pygame.draw.line(screen, (0, 0, 0), (x*100+20, y*100+20), ((x+1)*100-20, (y+1)*100-20), 2)
                pygame.draw.line(screen, (0, 0, 0), ((x+1)*100-20, y*100+20), (x*100+20, (y+1)*100-20), 2)
            elif cell == 'O':
                pygame.draw.circle(screen, (0, 0, 0), (x*100+50, y*100+50), 40, 2)
    for i in range(1, 3):
        pygame.draw.line(screen, (0, 0, 0), (i*100, 0), (i*100, 300), 2)
        pygame.draw.line(screen, (0, 0, 0), (0, i*100), (300, i*100), 2)
    pygame.display.flip()

def check_winner(board):
    for row in board:
        if row.count(row[0]) == len(row) and row[0] != '':
            return row[0]
    for col in range(len(board[0])):
        check = []
        for row in board:
            check.append(row[col])
        if check.count(check[0]) == len(check) and check[0] != '':
            return check[0]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != '':
        return board[0][2]
    return ''

def start_game():
    pygame.init()
    screen = pygame.display.set_mode((300, 300))
    pygame.display.set_caption('Tic Tac Toe')
    board = [['' for _ in range(3)] for _ in range(3)]
    turn = 'X'

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                x //= 100
                y //= 100
                if board[y][x] == '':
                    board[y][x] = turn
                    winner = check_winner(board)
                    if winner != '':
                        print(f'{winner} has won the game!')
                        pygame.time.wait(3000)
                        pygame.quit()
                        sys.exit()
                    turn = 'O' if turn == 'X' else 'X'
        draw_board(board, screen)

start_game()
