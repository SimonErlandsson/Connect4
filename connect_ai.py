from json.encoder import INFINITY
import random
import requests
import numpy as np
import argparse
import sys

# -----GAME LOGIC-----


def get_available_actions(state):
    available = [i for i in range(len(state[0])) if state[0][i] == 0]
    random.shuffle(available)
    return available


def apply_action(state, action, player):
    new_state = np.copy(state)
    row = 0
    while row < len(state) - 1 and state[row + 1][action] == 0:
        row += 1
    new_state[row][action] = player
    return new_state


# ------EVALUATION FUNCTION & CHUNKING-------
def utility(state):
    score = 0
    rows = len(state)
    cols = len(state[0])
    for row in range(rows):
        for col in range(cols):
            pos = (row, col)

            # Check chunks of four
            for chunk in get_chunks(state, pos, 4):
                score += evaluate_chunk(chunk, 1) - evaluate_chunk(chunk, -1)

    return score


def evaluate_chunk(chunk, player):
    if chunk.count(player) == 2 and chunk.count(0) == 2:  # two
        return 1
    elif chunk.count(player) == 3 and chunk.count(0) == 1:  # three
        return 5
    elif chunk.count(player) == 4:  # winning
        return 1000
    return 0


def is_anyone_winning(state):
    return True if get_who_is_winning(state) != 0 else False


def get_who_is_winning(state):
    rows = len(state)
    cols = len(state[0])
    for row in range(rows):
        for col in range(cols):
            pos = (row, col)
            for chunk in get_chunks(state, pos, 4):
                if chunk.count(1) == 4:
                    return 1
                elif chunk.count(-1) == 4:
                    return -1
    return 0


def get_chunks(state, pos, size):
    chunks = []
    max_row = len(state) - 1
    max_col = len(state[0]) - 1

    # Vertical (up-down)
    if pos[0] + (size - 1) <= max_row:
        chunks.append([state[pos[0] + i][pos[1]] for i in range(size)])

    # Horizontal (left-right)
    if pos[1] + (size - 1) <= max_col:
        chunks.append([state[pos[0]][pos[1] + i] for i in range(size)])

    # Diagonal \ (down right)
    if pos[0] + (size - 1) <= max_row and pos[1] + (size - 1) <= max_col:
        chunks.append([state[pos[0] + i][pos[1] + i] for i in range(size)])

    # Anti-diagonal / (down left)
    if pos[0] + (size - 1) <= max_row and pos[1] - (size - 1) >= 0:
        chunks.append([state[pos[0] + i][pos[1] - i] for i in range(size)])

    return chunks


# --------MIN-MAX----------
MAX_DEPTH = 5


def min_max_value(state):
    max_util = -INFINITY
    max_a = -1
    for a in get_available_actions(state):
        new_state = apply_action(state, a, 1)
        score = min_value(new_state, -INFINITY, INFINITY, 1)
        if (score > max_util):
            max_util = score
            max_a = a
    return max_a


def max_value(state, alpha, beta, depth):
    if (depth == MAX_DEPTH or is_anyone_winning(state)):
        return utility(state)

    v = -INFINITY
    for a in get_available_actions(state):
        new_state = apply_action(state, a, 1)
        v = max(v, min_value(new_state, alpha, beta, depth + 1))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v


def min_value(state, alpha, beta, depth):
    if (depth == MAX_DEPTH or is_anyone_winning(state)):
        return utility(state)

    v = INFINITY
    for a in get_available_actions(state):
        new_state = apply_action(state, a, -1)
        v = min(v, max_value(new_state, alpha, beta, depth + 1))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v
