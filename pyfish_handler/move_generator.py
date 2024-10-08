# pylint: disable=trailing-whitespace
# pylint: disable=missing-module-docstring
# pylint: disable=invalid-name
# pylint: disable=no-member
# pylint: disable=missing-final-newline
# pylint: disable=attribute-defined-outside-init
# pylint: disable=consider-using-enumerate
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=import-error
# pylint: disable=line-too-long

# project
from bit_master import BitMaster
from pieces import Pieces
from board import Board
from move import Move

class MoveGenerator:
    """ Handles all legal move generation for a given board state
    """
    @staticmethod
    def legal_pawn_moves(board: Board) -> list[Move]:
        """ Generates the legal pawn moves for a given board state
        reference: https://www.chessprogramming.org/Pawn_Pattern_and_Properties

        Args:
            board (Board): The board state

        Returns:
            list[Move]: A list of the legal moves
        """
        # initialize color
        color = Pieces.WHITE if board.turn else Pieces.BLACK
        pawns = board[color | Pieces.PAWN]
        second_rank = 0xff00 if board.turn else 0x00ff000000000000

        # single pawn push (shift the pawn bitboard upwards and mask it with the empty tiles)
        single_push_targets = BitMaster.shift_vertical(pawns, 1, color) & board[Pieces.EMPTY]
        
        # double pawn push
        double_push_targets = BitMaster.shift_vertical(pawns & second_rank, 2, color) & board[Pieces.EMPTY]

        board.display_bitboard(single_push_targets | double_push_targets)

if __name__ == '__main__':
    test_board = Board("rnbqkbnr/pp1p1ppp/2p5/2P5/1P2p3/P7/3PPPPP/RNBQKBNR w KQkq - 0 1")
    MoveGenerator.legal_pawn_moves(test_board)