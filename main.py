import numpy as np
import connect_ai
import pygame
pygame.init()
pygame.font.init()

# GAME STATICS
BLOCK_SIZE = 100
BOARD_SIZE = (6, 7)
BORDER_SIZE = 1

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GAME_FONT = pygame.font.SysFont('Comic Sans MS', 60)


def is_finished(board):
    winner = connect_ai.get_who_is_winning(board)
    if len(connect_ai.get_available_actions(board)) == 0:
        print("Draw!")
        return True, "It's a draw!", WHITE
    elif winner != 0:
        if winner == -1:
            print("You won!")
            return True, "You won!", GREEN
        else:
            print("You lost!")
            return True, "You lost...!", RED
    return False, "", WHITE


def game_loop(screen):
    running = True
    clock = pygame.time.Clock()
    board = np.zeros(BOARD_SIZE, dtype=int)
    is_player_move = True
    game_ended = False
    info_text = ""
    text_color = WHITE
    while running:
        # do AI move
        if not is_player_move:
            # -1 is player, 1 is ai
            ai_action = connect_ai.min_max_value(board)
            board = connect_ai.apply_action(board, ai_action, 1)
            game_ended, info_text, text_color = is_finished(board)
            is_player_move = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                # do player move
                if is_player_move and not game_ended:
                    action = pygame.mouse.get_pos()[0] // 100
                    if action in connect_ai.get_available_actions(board):
                        board = connect_ai.apply_action(board, action, -1)
                        game_ended, info_text, text_color = is_finished(board)
                        is_player_move = False

                # reset for new game
                if game_ended:
                    board = np.zeros(BOARD_SIZE, dtype=int)
                    is_player_move = True
                    info_text = ""
                    text_color = WHITE
                    game_ended = False

        screen.fill(WHITE)
        for y in range(len(board)):
            for x in range(len(board[0])):
                color = BLACK
                if board[y][x] == -1:
                    color = GREEN
                elif board[y][x] == 1:
                    color = RED
                pygame.draw.rect(
                    screen, WHITE, [x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE], 0)
                pygame.draw.rect(
                    screen, color, [x * BLOCK_SIZE + BORDER_SIZE, y * BLOCK_SIZE + BORDER_SIZE, BLOCK_SIZE - 2 * BORDER_SIZE, BLOCK_SIZE - 2 * BORDER_SIZE], 0)

        if info_text != "":
            textsurface = GAME_FONT.render(info_text, False, text_color)
            screen.blit(textsurface, (200, 200))
        pygame.display.flip()

    clock.tick(60)


def main():
    size = np.flip(BLOCK_SIZE * np.array(BOARD_SIZE))
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Connect 4 - AI")
    game_loop(screen)
    pygame.quit()


main()
