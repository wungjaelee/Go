from constants import *
from point import Point
from board import Board
import rule_checker as rc


class RegisterBlack(object):
    def act(self, container):
        try:
            name = container.black_player.register()
            container.results.append(name)
            container.black_player_name = name
            container.next_action = RegisterWhite()
        except RuntimeError:
            container.next_action = BlackIllegalMove()


class RegisterWhite(object):
    def act(self, container):
        try:
            name = container.white_player.register()
            container.results.append(name)
            container.white_player_name = name
            container.next_action = ReceiveStonesBlack()
        except RuntimeError:
            container.next_action = WhiteIllegalMove()


class ReceiveStonesBlack(object):
    def act(self, container):
        container.black_player.receive_stones(BLACK)
        container.next_action = ReceiveStonesWhite()


class ReceiveStonesWhite(object):
    def act(self, container):
        container.white_player.receive_stones(WHITE)
        container.next_action = MakeAMoveBlack()


class MakeAMoveBlack(object):
    def act(self, container):
        container.results.append(container.boards)
        try:
            response = container.black_player.make_a_move(container.boards)
            if response == PASS and rc.is_move_legal(BLACK, PASS):
                if container.previous_move_was_pass:
                    container.next_action = LegalEnd()
                else:
                    container.previous_move_was_pass = True
                    container.boards = [container.boards[0], *container.boards[0:2]]
                    container.next_action = MakeAMoveWhite()
            elif isinstance(response, Point) and rc.is_move_legal(BLACK, (response, container.boards)):
                container.previous_move_was_pass = False
                new_board = rc.get_board_if_valid_play(container.boards[0], BLACK, response)
                container.boards = [new_board, *container.boards[0:2]]
                container.next_action = MakeAMoveWhite()
            else:
                container.next_action = BlackIllegalMove()
        except RuntimeError:
            container.next_action = BlackIllegalMove()


class MakeAMoveWhite(object):
    def act(self, container):
        container.results.append(container.boards)
        try:
            response = container.white_player.make_a_move(container.boards)
            if response == PASS and rc.is_move_legal(WHITE, PASS):
                if container.previous_move_was_pass:
                    container.next_action = LegalEnd()
                else:
                    container.previous_move_was_pass = True
                    container.boards = [container.boards[0], *container.boards[0:2]]
                    container.next_action = MakeAMoveBlack()
            elif isinstance(response, Point) and rc.is_move_legal(WHITE, (response, container.boards)):
                container.previous_move_was_pass = False
                new_board = rc.get_board_if_valid_play(container.boards[0], WHITE, response)
                container.boards = [new_board, *container.boards[0:2]]
                container.next_action = MakeAMoveBlack()
            else:
                container.next_action = WhiteIllegalMove()
        except RuntimeError:
            container.next_action = WhiteIllegalMove()


class BlackIllegalMove(object):
    def act(self, container):
        container.results.append([container.white_player_name])


class WhiteIllegalMove(object):
    def act(self, container):
        container.results.append([container.black_player_name])


class LegalEnd(object):
    def act(self, container):
        scores = rc.get_scores(container.boards[0])
        if scores["B"] > scores["W"]:
            container.results.append([container.black_player_name])
        elif scores["W"] > scores["B"]:
            container.results.append([container.white_player_name])
        else:
            container.results.append([container.black_player_name,
                                        container.white_player_name])


class GameStateContainer(object):
    def __init__(self, black_player, white_player):
        self.next_action = RegisterBlack()
        self.black_player = black_player
        self.white_player = white_player
        self.black_player_name = None
        self.white_player_name = None
        self.boards = [Board()]
        self.results = []
        self.previous_move_was_pass = False

    
    def act(self, *args):
        self.next_action.act(self, *args)


    def get_results(self):
        return self.results