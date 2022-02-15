# Connect4
A Connect Four (Four in a row) graphical interface with AI. The game is playable by running main.py, using "python main.py".

<img src="connect.png" width="200">

Dependencies required are numpy and pygame.

The AI is based on mini-max with alpha-beta pruning. In the algorithm, the utility function used calculates the score of the current state as:

    Four in a row: +1000
    Three markers and one blank in chunk of four: +5
    Two markers and two blanks in chunk of four: +1

This is done for both the player and AI, and the resulting score is the difference.