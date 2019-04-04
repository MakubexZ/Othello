import time
import copy
import random
import math


class MCTS(object):
    """
    AI player by using Monte Carlo Tree Search with UCB
    """

    def __init__(self, board, opfor, time=3, max_actions=10000):
        self.board = board
        self.color = ['X', 'O'][opfor.color == 'X']
        self.play_turn = [self.color, opfor.color]
        # print(self.play_turn)
        self.player = self.color
        self.calculation_time = float(time)
        self.max_action = max_actions
        self.confident = 1.414
        self.plays = {}
        self.wins = {}
        self.max_depth = 1

    def move(self, board, action, player):
        # print(self.color)
        flipped_pos = board._move(action, player)
        # print(flipped_pos)
        return flipped_pos

    def unmove(self, board, action, flipped_pos):
        board._unmove(action, flipped_pos, self.color)
        # return board._board

    def get_action(self):
        action_list = list(self.board.get_legal_action(self.color))
        # print(action_list)
        if not action_list:
            return None, None
        self.plays = {}
        self.wins = {}
        simulations = 0
        begin = time.time()
        while time.time() - begin < self.calculation_time:
            board_copy = copy.deepcopy(self.board)
            play_turn_copy = copy.deepcopy(self.play_turn)
            self.run_simulation(board_copy, play_turn_copy)
            simulations += 1
        print('total simulations=', simulations)
        print('Maximum depth searched:', self.max_depth)
        action = self.select_one_move()
        # print(action)
        return None, action

    def run_simulation(self, board, play_turn):
        # color = self.color
        plays = self.plays
        wins = self.wins
        # print(action_list)
        player = self.get_player(play_turn)
        # print(player)
        visited_states = set()
        winner = -1
        expand = True
        for t in range(1, self.max_action + 1):
            action_list = list(board.get_legal_action(player))
            # print(action_list)
            # print(plays)
            '''
            if board.teminate():
                winner = self.board.get_winner()
                break
            '''
            if not action_list:
                player = self.get_player(play_turn)
                continue
            elif all(plays.get((player, action)) for action in action_list):
                log_total = math.log(sum(plays[(player, action)] for action in action_list))
                value, action = max(((wins[(player, action)] / plays[(player, action)]) + math.sqrt(self.confident * log_total / plays[(player, action)]), action) for action in action_list)
                # print(value, action)
            else:
                action = random.choice(action_list)
            # print(action)
            self.move(board, action, player)
            # print(flipped_pos)
            # self.unmove(board, action, flipped_pos)
            # print(board._board)
            # board.print_b()
            if expand and (player, action) not in plays:
                expand = False
                plays[(player, action)] = 0
                wins[(player, action)] = 0
                if t > self.max_depth:
                    self.max_depth = t
            visited_states.add((player, action))
            if board.teminate():
                winner = self.board.get_winner()
                break
            player = self.get_player(play_turn)
            # self.color = ['X', 'O'][player.color == 'X']
            # print(player)
        for player, action in visited_states:
            if (player, action) not in plays:
                continue
            plays[(player, action)] += 1
            # print(plays)
            winner_color = ['X', 'O', 'Draw'][winner]
            if player == winner_color:
                wins[(player, action)] += 1
            # print(wins)

    def get_player(self, play_turn):
        p = play_turn.pop(0)
        play_turn.append(p)
        return p

    def select_one_move(self):
        action_list = list(self.board.get_legal_action(self.color))
        if not action_list:
            return None
        percent_wins, action = max((self.wins.get((self.player, action), 0) / self.plays.get((self.player, action), 1), action) for action in action_list)
        # print(percent_wins, action)
        return action