# pylint: disable=trailing-whitespace
# pylint: disable=missing-module-docstring
# pylint: disable=missing-final-newline
# pylint: disable=wildcard-import
# pylint: disable=import-error

from typing import TypeAlias, Self

UInt4: TypeAlias = int

class CastlingRights(UInt4):
    """ Represents the castling rights for a player with a 4 bit integer.
    The bits represent the following information
    - Bit 0: King-side castling for white
    - Bit 1: Queen-side castling for white
    - Bit 2: King-side castling for black
    - Bit 3: Queen-side castling for black
    """
    
    MASKS = {
        "K": 0b1000,
        "Q": 0b0100,
        "k": 0b0010,
        "q": 0b0001
    }
    
    def __new__(cls, value: int) -> None:
        cls._validate(value)
        return super().__new__(cls, value)

    @classmethod
    def _validate(cls, value: int):
        if not (isinstance(value, int) and 0 <= value <= 15):
            error = f"Castling rights must be an integer between 0 and 15, got '{value}'"
            raise ValueError(error)
        
    def __repr__(self) -> str:
        return f"CastlingRights({self.__str__()})"
        
    def __str__(self) -> str:
        text = ""
        for symbol, mask in self.MASKS.items():
            if self & mask != 0:
                text += symbol
        if text == "":
            text = "-"
        return text
    
    @classmethod
    def from_text(cls, text: str) -> Self:
        """ Generates a CastlingRights object from FEN encoding

        Args:
            text (str): The fourth-to-last term in any given FEN encoding

        Returns:
            Self: The CastlingRights object with the encoded information
        """
        if text == "-":
            return cls(0)
        out = 0
        for symbol, mask in cls.MASKS.items():
            if symbol in text:
                out |= mask
        return cls(out)
    
    def disable_white(self) -> Self:
        """ Returns a copy of the object without white castling rights """
        return CastlingRights(int(self) & 0b11)
    
    def disable_black(self) -> Self:
        """ Returns a copy of the object without black castling rights """
        return CastlingRights(int(self) & 0b1100)
    
    @property
    def white_king_side(self) -> bool:
        """ Returns True if the white king can castle king-side

        Returns:
            bool: Whether the white king can castle king-side
        """
        return bool(int(self) & 0x1)
    
    @property
    def white_queen_side(self) -> bool:
        """ Returns True if the white king can castle queen-side

        Returns:
            bool: whether the white king can castle queen-side
        """
        return bool(int(self) & 0x2)
    
    @property
    def black_king_side(self) -> bool:
        """ Returns True if the black king can castle king-side

        Returns:
            bool: Whether the black king can castle king-side
        """
        return bool(int(self) & 0x4)
    
    @property
    def black_queen_side(self) -> bool:
        """ Returns True if the black king can castle queen-side

        Returns:
            bool: Whether the black king can castle queen-side
        """
        return bool(int(self) & 0x8)