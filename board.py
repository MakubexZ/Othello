class Board(object):
    def __init__(self):
        self.empty = '.'
        self._board = [[self.empty for _ in range(8)] for _ in range(8)]
        self._board[3][4], self._board[4][3] = 'X', 'X'
        self._board[3][3], self._board[4][4] = 'O', 'O'

    def print_b(self):
        board = self._board
        print(' ', ' '.join(list('ABCDEFGH')))
        for i in range(8):
            print(str(i+1), ' '.join(board[i]))
        # print('\n')

    def __getitem__(self, index):
        return self._board[index]

    def teminate(self):
        list1 = list(self.get_legal_action('X'))
        list2 = list(self.get_legal_action('O'))
        return[False, True][len(list1) == 0 and len(list2) == 0]

    def get_winner(self):
        s1, s2 = 0, 0
        for i in range(8):
            for j in range(8):
                if self._board[i][j] == 'X':
                    s1 += 1
                if self._board[i][j] == 'O':
                    s2 += 1
        if s1 > s2:
            return 0
        if s1 < s2:
            return 1
        if s1 == s2:
            return 2

    def _move(self, action, color):
        x, y = action
        # print(action)
        self._board[x][y] = color
        return self._flip(action, color)

    def _flip(self, action, color):
        flipped_pos = []
        for line in self._get_lines(action):
            # print(line)
            for i, p in enumerate(line):
                if self._board[p[0]][p[1]] == self.empty:
                    break
                elif self._board[p[0]][p[1]] == color:
                    flipped_pos.extend(line[:i])
                    break
        # if
        # print(flipped_pos)
        assert len(flipped_pos) > 0
        for p in flipped_pos:
            self._board[p[0]][p[1]] = color
        # print(flipped_pos)
        return flipped_pos

    def _unmove(self, action, flipped_pos, color):
        self._board[action[0]][action[1]] = self.empty
        uncolor = ['X', 'O'][color == 'X']
        for p in flipped_pos:
            self._board[p[0]][p[1]] = uncolor

    def _get_lines(self, action):
        board_coord = [(i, j) for i in range(8) for j in range(8)]

        r, c = action
        ix = r*8+c
        r, c = ix//8, ix % 8

        left = board_coord[r*8:ix]
        right = board_coord[ix+1:(r+1)*8]
        top = board_coord[c:ix:8]
        bottom = board_coord[ix+8:8*8:8]

        if r <= c:
            lefttop = board_coord[c-r:ix:9]
            rightbottom = board_coord[ix+9:(7-(c-r))*8+7+1:9]
        else:
            lefttop = board_coord[(r-c)*8:ix:9]
            rightbottom = board_coord[ix+9:7*8+(7-(c-r))+1:9]
        if r+c <= 7:
            leftbottom = board_coord[ix+7:(r+c)*8+1:7]
            righttop = board_coord[r+c:ix:7]
        else:
            leftbottom = board_coord[ix+7:7*8+(r+c)-7+1:7]
            righttop = board_coord[((r+c)-7)*8+7:ix:7]

        left.reverse()
        top.reverse()
        lefttop.reverse()
        righttop.reverse()
        lines = [left, top, lefttop, righttop, right, bottom, leftbottom, rightbottom]
        # print(lines)
        return lines

    def _can_fliped(self, action, color):
        flipped_pos = []
        # print(action)
        # n = 0
        for line in self._get_lines(action):
            '''
            t = ['left', 'top', 'lefttop', 'righttop', 'right', 'bottom', 'leftbottom', 'rightbottom']
            print(t[n])
            n = n + 1
            print(line)
            '''
            for i, p in enumerate(line):
                if self._board[p[0]][p[1]] == self.empty:
                    # print(i, p)
                    break
                elif self._board[p[0]][p[1]] == color:
                    flipped_pos.extend(line[:i])
                    # print (flipped_pos)
                    break
            # print(flipped_pos)
        return [False, True][len(flipped_pos) > 0]

    def get_legal_action(self, color):
        uncolor = ['X', 'O'][color == 'X']
        uncolor_near_pos = []
        board = self._board
        for i in range(8):
            for j in range(8):
                if board[i][j] == uncolor:
                    for dx, dy in [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]:
                        x, y = i+dx, j+dy
                        if 0 <= x <= 7 and 0 <= y <= 7 and board[x][y] == self.empty and (x, y) not in uncolor_near_pos:
                            uncolor_near_pos.append((x, y))
        # print(uncolor_near_pos)
        for p in uncolor_near_pos:
            if self._can_fliped(p, color):
                yield p


if __name__ == '__main__':
    board = Board()
    board.print_b()
    print(list(board.get_legal_action('X')))
