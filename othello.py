from board import Board
from player import HumanPlayer, AIPlayer


class Game(object):
    def __init__(self):
        self.board = Board()
        self.current_player = None

    def make_two_players(self):
        while True:
            ps = input("Please select two player`s type:\n\t0.Human\n\t1.AI\nSuch as:0 0\n:")
            pss = ps.split(' ')
            if len(pss) != 2:
                print('\nWrong choice, please enter numbers as example')
                continue
            elif len(pss) == 2:
                p1, p2 = [int(p) for p in ps.split(' ')]
                if p1 > 1 or p2 > 1:
                    print('\nWrong choice, please enter numbers as example')
                    continue
                break
        while True:
            if p1 == 1 and p2 == 1:
                level_ix1 = int(input("Please select the level of AI player1.\n\t0: random\n\t1: minimax\n\t2: minimax_alphabeta\n\t3: MCTS3s\n\t4: MCTS?s\n:"))
                if level_ix1 > 4:
                    print('\nWrong choice, please enter numbers as behind')
                    continue
                level_ix2 = int(input("Please select the level of AI player2.\n\t0: random\n\t1: minimax\n\t2: minimax_alphabeta\n\t3: MCTS3s\n\t4: MCTS?s\n:"))
                if level_ix2 > 4:
                    print('\nWrong choice, please enter numbers as behind')
                    continue
                player1 = AIPlayer('X', level_ix1)
                player2 = AIPlayer('O', level_ix2)
                break
            elif p1 == 1 or p2 == 1:
                level_ix = int(input("Please select the level of AI player.\n\t0: random\n\t1: minimax\n\t2: minimax_alphabeta\n\t3: MCTS3s\n\t4: MCTS?s\n:"))
                if level_ix > 4:
                    print('\nWrong choice, please enter numbers as behind')
                    continue
                else:
                    if p1 == 0:
                        player1 = HumanPlayer('X')
                        player2 = AIPlayer('O', level_ix)
                        break
                    elif p2 == 0:
                        player1 = AIPlayer('X', level_ix)
                        player2 = HumanPlayer('O')
                        break
            else:
                player1, player2 = HumanPlayer('X'), HumanPlayer('O')
                break
        return player1, player2

    def switch_player(self, player1, player2):
        if self.current_player is None:
            return player1
        else:
            return [player1, player2][self.current_player == player1]

    def print_winner(self, winner):
        print(['Winner is player1', 'Winner is player2', 'Draw'][winner])
        print('\n\n')

    def run(self):
        flag = 0
        player1, player2 = self.make_two_players()
        print('\nGame start!\n')
        self.board.print_b()
        while True:
            print('\n')
            self.current_player = self.switch_player(player1, player2)
            action = self.current_player.think(self.board)
            if action == [9, 9]:
                print('Player chose pass')
                if flag == 0:
                    flag = 1
                    continue
                elif flag == 1:
                    winner = self.board.get_winner()
                    break
            else:
                flag = 0
            if action is not None:
                self.current_player.move(self.board, action)
                # print(o)
            # print(self.board)
            self.board.print_b()
            if self.board.teminate():
                winner = self.board.get_winner()
                break
        print('\nGame over!\n')
        self.print_winner(winner)


if __name__ == '__main__':
    Game().run()