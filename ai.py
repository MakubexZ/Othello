import random
import MCTS
import MCTS_selection

class AI(object):

    def __init__(self, level_ix=0):
        self.level = ['random', 'minimax', 'minimax_alphabeta', 'MCTS3s', 'MCTS?s'][level_ix]
        # 棋盘位置权重，参考：https://github.com/k-time/ai-minimax-agent/blob/master/ksx2101.py
        self.board_weights = [
            [120, -20,  20,   5,   5,  20, -20, 120],
            [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
            [20,  -5,  15,   3,   3,  15,  -5,  20],
            [5,  -5,   3,   3,   3,   3,  -5,   5],
            [5,  -5,   3,   3,   3,   3,  -5,   5],
            [20,  -5,  15,   3,   3,  15,  -5,  20],
            [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
            [120, -20,  20,   5,   5,  20, -20, 120]
        ]

    def evaluate(self, board, color):
        uncolor = ['X', 'O'][color == 'X']
        score = 0
        for i in range(8):
            for j in range(8):
                if board[i][j] == color:
                    score += self.board_weights[i][j]
                elif board[i][j] == uncolor:
                    score -= self.board_weights[i][j]
        return score

    def brain(self, board, opponent):
        if self.level == 'random':
            _, action = self.randomchoice(board)
        elif self.level == 'minmax':
            _, action = self.minimax(board, opponent)
        elif self.level == 'minimax_alphabeta':
            _, action = self.minimax_alpha_beta(board, opponent)
        elif self.level == 'MCTS3s':
            ai = MCTS.MCTS(board, opponent)
            _, action = ai.get_action()
        else:
            ai = MCTS_selection.MCTS(board, opponent)
            _, action = ai.get_action()
        # print(action)
        if action is None:
            action = [9, 9]
        # assert action is not None, 'action is None'
        return action

    def randomchoice(self, board):
        color = self.color
        action_list = list(board.get_legal_action(color))
        if not action_list:
            return None, None
        return None, random.choice(action_list)

    def minimax(self, board, opfor, depth=4):
        color = self.color
        if depth == 0:
            return self.evaluate(board, color), None
        action_list = list(board.get_legal_action(color))
        if not action_list:
            return self.evaluate(board, color), None
        best_score = -10000
        best_action = None
        for action in action_list:
            flipped_pos = self.move(board, action)
            # print(flipped_pos)
            score, _ = opfor.minimax(board, self, depth-1)
            self.unmove(board, action, flipped_pos)
            # print(board._board)
            score = -score
            if score > best_score:
                best_score = score
                best_action = action
        return best_score, best_action

    def minimax_alpha_beta(self, board, opfor, depth=4, my_best=-float('inf'), opp_best=float('inf')):
        color = self.color
        if depth == 0:
            return self.evaluate(board, color), None
        action_list = list(board.get_legal_action(color))
        if not action_list:
            return self.evaluate(board, color), None
        best_score = my_best
        best_action = None
        for action in action_list:
            flipped_pos = self.move(board, action)
            score, _ = opfor.minimax_alpha_beta(board, self, depth-1, -opp_best, -best_score)
            self.unmove(board, action, flipped_pos)
            score = -score
            if score > best_score:
                best_score = score
                best_action = action
            if best_score > opp_best:
                break
        return best_score, best_action

