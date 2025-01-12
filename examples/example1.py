# pylint: disable=trailing-whitespace
# pylint: disable=missing-module-docstring
# pylint: disable=missing-final-newline
# pylint: disable=wildcard-import
# pylint: disable=import-error
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

# project
from src import Board, Move, Flags, squares
import src as chess

class Bot:
    @staticmethod
    def get_best_move(_: Board, __: float) -> None:
        return Move(Flags.QUIET, squares.NONE, squares.NONE)

chess.start_game(
    white = chess.User,
    black = Bot.get_best_move,
    position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    screen_size = (1280, 720),
    orientation = chess.WHITE
)