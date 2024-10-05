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
- The purpose of this project is to create a relatively fast chess engine without compromising code readability.
- The name "pyfish" is a play on the words "python" and "stockfish" (a popular chess engine).

## Implementations
- The board states are represented with twelve unsigned 64-bit integers
    - reference: https://www.chessprogramming.org/Bitboards
- Moves are represented with 16 bit integers.
    - 4 bits for the 14 different types of moves (captures, en-passant, castling, ect)
    - 6 bits for the starting square
    - 6 bits for the target square
    - reference: https://www.chessprogramming.org/Encoding_Moves

## References
https://www.chessprogramming.org
