# pylint: disable=trailing-whitespace
# pylint: disable=missing-module-docstring
# pylint: disable=invalid-name
# pylint: disable=no-member
# pylint: disable=missing-final-newline
# pylint: disable=attribute-defined-outside-init
# pylint: disable=consider-using-enumerate
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import

def display_bitboard(bitboard: int) -> None:
    """ Displays the given bitboard to the CLI
    Args:
        bitboard (np.uint64): The 64 bit board to display
    """
    print(bitboard)
    bitboard = bin(bitboard)[2:].rjust(64, '0')
    for row in range(8):
        for tile in range(7, -1, -1):
            print(f'{bitboard[row*8+tile]} ', end='')
        print(f'| {8-row}')
    print('----------------+')
    print('a b c d e f g h')