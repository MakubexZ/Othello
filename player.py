from ai import AI
import time


class Player(object):
    def __init__(self, color):
        self.color = color

    def think(self, board):
        pass

    def move(self, board, action):
        flipped_pos = board._move(action, self.color)
        # print(flipped_pos)
        return flipped_pos

    def unmove(self, board, action, flipped_pos):
        board._unmove(action, flipped_pos, self.color)


class HumanPlayer(Player):
    def __init__(self, color):
        super().__init__(color)

    def think(self, board):
        while True:
            # print(list(board.get_legal_action(self.color)))
            action = input("Turn to '{}'.\nPlease enter a point.(such as 'A1'):".format(self.color))
            # print(action)
            if action != 'pass' and len(action) != 2:
                print('Wrong input, please enter numbers as example')
                continue
            elif action == 'pass':
                return [9, 9]
            else:
                r, c = action[1], action[0].upper()
                if r in '12345678' and c in 'ABCDEFGH':
                    x, y = '12345678'.index(r), 'ABCDEFGH'.index(c)
                    if (x, y) in board.get_legal_action(self.color):
                        return x, y
                    else:
                        print('This position has been chosen, or maybe its not a optional position, please enter again')
                        continue
                else:
                    print('Wrong input, please enter numbers as example')
                    continue


class AIPlayer(Player, AI):
    def __init__(self, color, level_ix=0):
        super().__init__(color)
        super(Player, self).__init__(level_ix)

    def think(self, board):
        print("Turn to '{}'.\nPlease wait a moment. AI is thinking...".format(self.color))
        begin = time.time()
        uncolor = ['X', 'O'][self.color == 'X']
        opfor = AIPlayer(uncolor)
        # print(list(board.get_legal_action(self.color)))
        action = self.brain(board, opfor)
        # print(action)
        if action == [9, 9]:
            return action
        c, r = action[0], action[1]
        # print(action[0], action[1])
        abscissa = 'ABCDEFGH'
        ordinate = '12345678'
        x, y = abscissa[r], ordinate[c]
        print('AI chose ', x, y)
        time_consuming = time.time() - begin
        print('Time consuming is ', "%.2f" % time_consuming)
        return action