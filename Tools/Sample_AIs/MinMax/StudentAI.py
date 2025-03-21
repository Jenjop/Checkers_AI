from BoardClasses import Board
from random import randint


# The following part should be completed by students.
# Students can modify anything except the class name and exisiting functions and varibles.
search_depth = 6#Search depth for recursive func

class Tree():
    def __init__(self, color, move=None):
        self.color = color
        self.move = move
        self.value = None
        self.children = []


class StudentAI():

    def __init__(self, col, row, p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col, row, p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1: 2, 2: 1}
        self.color = 2

    def get_move(self, move):
        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])  # Run opponent's move for self.board
        else:
            self.color = 1

        root = Tree(self.opponent[self.color]) #Tree root
        self.rec_tree(root, search_depth)#Set up tree
        self.rec_min_max_heuristic(root)

        avail_moves = root.value[list(root.value)[0]]
        #cur_move = avail_moves[0]
        cur_move = avail_moves[randint(0,len(avail_moves)-1)]
        #print(avail_moves)

        self.board.make_move(cur_move, self.color)  # Make the optimal move
        move = cur_move
        return move

    def ftu(self, color): #Function to use (min vs max by color)
        if color == self.color:  # Calculate Min
            return max
        else:  # Calculate Max
            return min

    def min_max(self, children, color):  # Returns dict -> {Max/min value: Moves to get here}
        ftu = self.ftu(color) #Use corresponding min or max depending on color
        value_map = {}
        for child in children:
            for v in child.value.keys():
                value_map.setdefault(v, []).append(child.move)  # D: {heuristic value: Move to make to get here}
        # print(value_map)
        return {ftu(value_map): value_map[ftu(value_map)]}

    def board_points(self):  # 5 + row number for pawns, 5 + row number + 2 for kings
        '''
        def board_points(self):  # 5 + row number for pawns, 5 + row number + 2 for kings
            king_pts_value = 5 + (
                        self.row - 1) + 2  # 5 pts for piece, self.row -1 pts for pts at end of board, + 1 for being king
            pts = 0
            for i in range(self.row):
                for j in range(self.col):
                    checker = self.board.board[i][j]
                    if checker.color == 'B':  # For black side pieces
                        if checker.is_king:
                            pts += king_pts_value
                        else:
                            pts += 5 + checker.row
                    elif checker.color == 'W':  # FOr white side pieces
                        # pts -= (11 - checker.row)  # 5 + (6 - Row)
                        if checker.is_king:
                            pts -= king_pts_value
                        else:
                            pts -= (5 + (
                                        self.row - checker.row - 1))  # 5 + (Num of rows - Row - 1) eg. 5x5 board, 5th row is 5(num) - 4(row) -1 = 0

            if abs(pts) > 2:
                self.dif_val = True
            # if debug: print(color(root.color), pts, -pts)
            return pts if self.color == 1 else -pts  # BLACK(1) GOES FIRST, so positive points, if self.color == white(2), then return white pieces as positive points
            '''
        pts = 0
        for i in range(self.row):
            for j in range(self.col):
                checker = self.board.board[i][j]
                if checker.color == 'B':  # For black side pieces
                    pts += 5 + checker.row
                    if checker.is_king:  # 2 additional pts for king
                        pts += 2
                elif checker.color == 'W':  # FOr white side pieces
                    pts -= 11 - checker.row  # 5 + (6 - Row)
                    if checker.is_king:  # 2 additional pts for king
                        pts -= 2
        return pts if self.color == 1 else -pts

    def print_tree(self, root, level=0):
        # print("PRINTING TREE")

        print("\t" * level, root.value, "->", root.move)
        if len(root.children) != 0:  # Not Leaf node
            for child in root.children:
                self.print_tree(child, level + 1)

    def rec_tree(self, root: Tree, level=1):#Create tree up to depth level
        if level == 0:
            pass
        else:
            if root.move is not None:  # Not root of tree
                self.board.make_move(root.move, root.color)
            #Check if win here maybe?
            avail_moves = self.board.get_all_possible_moves(self.opponent[root.color])
            for i in range(len(avail_moves)):
                for j in range(len(avail_moves[i])):
                    #print(root)
                    root.children.append( Tree(self.opponent[root.color], avail_moves[i][j] ) )
            for child in root.children:
                self.rec_tree(child, level - 1)

            if root.move is not None:
                self.board.undo()

    def rec_min_max_heuristic(self, root: Tree):#Apply min_max heuristic to tree
        if root.move is not None: #If not root of tree, make the move required to get here
            self.board.make_move(root.move, root.color)
        if len(root.children) == 0: #Passed node has no children
            pass #Evaluate heuristic for board(and return?)
            root.value = {self.board_points(): []}
        else: #Evaluate rec_heuristic for children, then retrieve values and apply min/max as appropriate
            for child in root.children:
                self.rec_min_max_heuristic(child)
            root.value = self.min_max(root.children, root.color)

        if root.move is not None:
            self.board.undo()


