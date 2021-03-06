# -*- coding: utf-8 -*-

"""
`chess` generate the chessboard and initiate the game
"""


# ///////////////////////////////////////////////////
# Python packages
from itertools import product
from copy import copy
# import math

# ---------------------------------------------------

# ///////////////////////////////////////////////////
# My modules
from app.chess.piece import King
from app.chess.piece import Queen
from app.chess.piece import Rook
from app.chess.piece import Bishop
from app.chess.piece import Knight
from app.chess.piece import ChessPiece
# ---------------------------------------------------

# ///////////////////////////////////////////////////


class Chess(object):
    """ Chess class """
    def __init__(self, params):
        self.solutions = 0
        self.width = params[0]
        self.height = params[1]
        self.dict_pieces = params[2]
        self.number_pieces = reduce(lambda x, y: x+y, params[2].values())
        # Create all pieces objects
        self.pieces = self.create_pieces(params[2])
        self.pieces_types = [i.get_symbol() for i in self.pieces]
        self.chessboard = Chessboard(self.width, self.height)

    def create_pieces(self, pieces_dict):
        """ Create pieces """
        kings_list = [King() for _ in xrange(pieces_dict['King'])]
        queens_list = [Queen() for _ in xrange(pieces_dict['Queen'])]
        rook_list = [Rook() for _ in xrange(pieces_dict['Rook'])]
        bishop_list = [Bishop() for _ in xrange(pieces_dict['Bishop'])]
        knight_list = [Knight() for _ in xrange(pieces_dict['Knight'])]
        pieces = list()
        pieces.extend(kings_list)
        pieces.extend(queens_list)
        pieces.extend(rook_list)
        pieces.extend(bishop_list)
        pieces.extend(knight_list)
        return pieces

    def print_solution_chessboard(self):
        """ print chess solution """
        pass

    def run_game(self):
        """ Initiate the Chessboard and starts the game """

        print "start game.."
        previous_piece = ChessPiece()
        if self.pieces:
            self.populate(previous_piece, self.pieces, self.chessboard)

        # duplicat = [math.factorial(x) for x in self.dict_pieces.values()]
        # self.solutions = (self.solutions)/reduce(lambda x, y: x*y, duplicat)
        self.print_solution_chessboard()

    def populate(self, previous_piece, pieces, chessboard):
        """
        Initiate the Chessboard and starts the game

        Keyword arguments:
        pieces -- the pieces that are not put on the chessboard
        chessboard -- the chessboard
        """

        remained_pieces = copy(pieces)
        current_piece = pieces[0]

        if chessboard.empty_squares:
            # Check all possible mouvments for a piece
            for empty_square in copy(chessboard.empty_squares):
                # move the piece in the chessboard
                current_piece.deplace_piece(empty_square)
                if chessboard.can_put_on(current_piece):
                    # Check if all pieces are in Board
                    current_piece.squares.append(empty_square)
                    current_piece.square = empty_square
                    if not check_duplicate(current_piece, previous_piece):
                        _leng = len(chessboard.allocated_pieces)+1
                        if _leng == len(self.pieces):
                            self.solutions += 1

                        else:
                            # fix the piece in the Chessboard
                            # populate with pieces except in the board
                            if current_piece in remained_pieces:
                                remained_pieces.remove(current_piece)

                            chessboard.allocated(current_piece)

                            self.populate(current_piece,
                                          remained_pieces, chessboard)
                            # Remove the piece from the Chessboard
                            # and range to the next empty square
                            chessboard.remove_piece(current_piece)

            current_piece.squares = list()
            current_piece.square = None


def check_duplicate(piece1, piece2):
    """ Check if the piece already allocated before  """
    if piece1.symbol == piece2.symbol and piece1.square in piece2.squares:
        return True
    else:
        return False


class Chessboard(object):
    """
    The chessboard class, manages and saves pieces moves and positions
    """

    # ///////////////////////////////////////////////////
    def __init__(self, width, height):
        """
        Attributes:
        `board`            -- All squares that formed the Chessboard.
        `allocated_squares`-- Squares reserved by pieces and their attack area.
        `allocated_pieces` -- The piece put on the ChessBoard.
        `empty_squares`    -- The current empty squares in the Chessboard
        """
        list_of_board = list(product(range(1, width+1), range(1, height+1)))
        self.board = [Square(x[0], x[1]) for x in list_of_board]

        self.allocated_squares = list()
        self.empty_squares = copy(self.board)
        self.allocated_pieces = list()

    def __update_allocated_squares(self, piece):
        """
        Updates piece positions on the chessboard
        """
        # Allocated piece square in the board
        for square in self.board:
            if square.coordinates() == piece.pos():
                self.allocated_squares.append(square)
                self.empty_squares.remove(square)
        # Allocated all square can be attacked
        for _square in copy(self.empty_squares):
            if piece.check_attack(_square):
                # print "piece {0} can attack {1} >>>".
                # format(piece.pos(),square.coordinates())
                self.allocated_squares.append(_square)
                self.empty_squares.remove(_square)

    def allocated(self, piece):
        """
        Updates the Chessboard after every piece's movement
        """
        if piece not in self.allocated_pieces:
            self.allocated_pieces.append(piece)
        self.__update_allocated_squares(piece)

    def remove_piece(self, piece):
        """Removes a piece from the chessboard"""
        self.allocated_pieces.remove(piece)
        self.allocated_squares = list()
        self.empty_squares = copy(self.board)
        new_pieces_list = copy(self.allocated_pieces)
        for new_p in new_pieces_list:
            self.allocated(new_p)

    def can_put_on(self, piece):
        """
        Checks whether the piece can attack
        other pieces in the Chessboard
        """
        test = True
        if self.allocated_pieces:
            for new_p in self.allocated_pieces:
                if new_p.pos() != piece.pos() and piece.check_attack(new_p):
                    test = False
                    break
        return test


class Square(object):
    """
    Represents a position on the Board
    """
    def __init__(self, x_cord, y_cord):
        """  initiate the square"""
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.is_allocated = None

    def coordinates(self):
        """ return coordinates of the square"""
        return (self.x_cord, self.y_cord)

    def allocate(self, piece):
        """ allocate square piece"""
        self.is_allocated = piece
