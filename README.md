<div align="center">
<pre>
   ▄███████▄ ▄██   ▄      ▄████████  ▄█     ▄████████    ▄█    █▄    
  ███    ███ ███   ██▄   ███    ███ ███    ███    ███   ███    ███   
  ███    ███ ███▄▄▄███   ███    █▀  ███▌   ███    █▀    ███    ███   
  ███    ███ ▀▀▀▀▀▀███  ▄███▄▄▄     ███▌   ███         ▄███▄▄▄▄███▄▄ 
▀█████████▀  ▄██   ███ ▀▀███▀▀▀     ███▌ ▀███████████ ▀▀███▀▀▀▀███▀  
  ███        ███   ███   ███        ███           ███   ███    ███   
  ███        ███   ███   ███        ███     ▄█    ███   ███    ███   
 ▄████▀       ▀█████▀    ███        █▀    ▄████████▀    ███    █▀    
</pre>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# This project is currently being developed

</div>

## Purpose

- This program is a chess engine created from scratch in python.
- The purpose of this project is to compete with the other python chess engines such as snakefish and sunfish. This project intends to go further than those projects and implement more advanced techniques such as iterative deepening and NNUE.
- The name "pyfish" is a play on the words "python" and "stockfish".

## Implementations
- 64 bit integers ([bitboards](https://www.chessprogramming.org/Bitboards)) are used instead of 8x8 lists ([mailbox approach](https://www.chessprogramming.org/Mailbox)) to represent the board state for a few reasons.
    - Manipulations can be done in parallel with bitwise operations. This is significantly faster than scanning arrays.
    - This does not mean that bitboards are the best possible approach to the problem, there are other techniques.
- Moves are represented with [16 bit integers](https://www.chessprogramming.org/Encoding_Moves).
    - 4 bits for the 14 different types of moves (captures, en-passant, castling, ect)
    - 6 bits for the starting square
    - 6 bits for the target square

## References
https://www.chessprogramming.org
