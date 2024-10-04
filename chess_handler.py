# pylint: disable=trailing-whitespace
# pylint: disable=missing-module-docstring
# pylint: disable=invalid-name
# pylint: disable=no-member
# pylint: disable=missing-final-newline
# pylint: disable=attribute-defined-outside-init
# pylint: disable=consider-using-enumerate
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import

from board import Board
from move import Move

class ChessHandler:
    """ This class implements the rules of chess.
    """
    @staticmethod
    def make_move(move: Move, board: Board) -> Board:
        """ Plays a move on a board and returns a new board

        Args:
            move (np.uint16): Information is at the top of the class
            bitboards (list[np.uint64]): A list of 12 bitboards

        Returns:
            list[np.uint64]: A list of 12 bitboards
        """
        
        piece = board.get_piece_at(move.initial_square)
        board.destroy_piece(move.initial_square)
        board.add_piece(move.target_square, piece)