# pylint: disable=trailing-whitespace
# pylint: disable=missing-module-docstring
# pylint: disable=missing-final-newline
# pylint: disable=wildcard-import
# pylint: disable=import-error

# standard
from typing import Callable

# third party
import pygame as pg

# project
from src.core.move import Move, Flags
from src.core.squares import WHITE
from src.core.board import Board

from src.renderer.board_renderer import BoardRenderer

class Mouse(pg.Vector2):
    """ Handles all mouse-related data """
    def __init__(self, board: Board, board_renderer: BoardRenderer) -> None:
        # reference
        self.board = board
        self.board_renderer = board_renderer
        
        # attributes
        self.position = pg.Vector2(0, 0)
        self.board_position = pg.Vector2(0, 0)
        self.tile_position = pg.Vector2(0, 0)
        self.last_move_square = None
        self.selected_square = None
        self.listeners = {
            "request_move": []
        }
        
        # super
        super().__init__(self.position)
        
    def update_board_state(self, board: Board) -> None:
        """ Updates the board state for this class """
        self.board = board
        
    def on_request_move(self, subscriber: Callable[[Move], None]) -> None:
        """ Calls the given function once a move is requested

        Args:
            subscriber (callable): The function to call when a move is requested
        """
        self.listeners["request_move"].append(subscriber)
    
    def deselect(self) -> None:
        """ Deselects the current tile """
        self.selected_square = None
    
    def click(self) -> None:
        """ Processes mouse data. This method should be called whenever the mouse is clicked. """
        self.position = pg.Vector2(pg.mouse.get_pos())
        self.board_position = self.position - self.board_renderer.POSITION
        self.tile_position = self.board_position // self.board_renderer.TILE_SIZE
        
        if self.board_renderer.orientation == WHITE:
            new_square = int(self.tile_position.x + (7 - self.tile_position.y) * 8)
        else:
            new_square = int((7 - self.tile_position.x) + self.tile_position.y * 8)
        
        piece = self.board.get_piece(new_square)
        if new_square == self.selected_square:
            # selecting same square - deselect
            self.deselect()
        elif self.selected_square is None and piece is not None:
            # selecting new square
            self.selected_square = new_square
        elif self.selected_square is not None:
            # selecting second square - make move and deselect
            self.request_move(self.selected_square, new_square)
            self.deselect()
    
    def request_move(self, initial_square: int, target_square: int) -> None:
        """ Requests a move to play

        Args:
            initial_square (int): The initial square of the move
            target_square (int): The target square of the move
        """
        # TODO: check if move is valid
        selected_piece = self.board.get_piece(target_square)
        if selected_piece is None:
            flag = Flags.QUIET
        else:
            flag = Flags.CAPTURE
        move = Move(flag, initial_square, target_square)
        for subscriber in self.listeners["request_move"]:
            subscriber(move)
    
    def save_last_move_square(self, square: int) -> None:
        """ Saves the square of the last move """
        self.last_move_square = square