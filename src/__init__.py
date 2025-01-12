# pylint: disable=trailing-whitespace
# pylint: disable=missing-module-docstring
# pylint: disable=missing-final-newline
# pylint: disable=import-error

# standard
from typing import TypeAlias

# third party
from pygame import Vector2

# project
from src.core.castling_rights import CastlingRights
from src.core.bitboard import Bitboard
from src.core.move import Move, Flags
from src.core.piece import Piece
from src.core.board import Board
from src.core.move_maker import MoveMaker
from src.core.squares import WHITE, BLACK
from src.core import squares

from src.renderer.app import App

# TODO: Make User into a class

User: TypeAlias = None
Fen: TypeAlias = str
Orientation: TypeAlias = bool

def start_game(
    white = User,
    black = User,
    position: Fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    screen_size: Vector2 = (640, 640),
    orientation: Orientation = True
) -> None:
    """ Starts a game of chess. Both players are set to human
    by default. In order to include a bot, a function must be
    passed in as either black or white. The function must be
    formatted like this.
    
    def get_random_move(board: Board, time_remaining: float) -> None:
        return random.choice(board.get_legal_moves(board))

    Args:
        orientation (Orientation): The direction the board is facing. Defaults to white
        white (_type_, optional): The player controller for white. Defaults to human.
        black (_type_, optional): The player controller for black. Defaults to human.
        position (Fen, optional): The starting position of the game.
        screen_size (Vector2, optional): The size of the app window. Defaults to 640x640.
    """
    app = App(white, black, position, screen_size, orientation)
    app.run()