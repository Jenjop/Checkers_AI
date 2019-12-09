from BoardClasses import Board
from random import randint

# The following part should be completed by students.
# Students can modify anything except the class name and exisiting functions and varibles.

'''
NOTES
Black goes first in 7x7 manual: "7" "7" "2" "m" "0"
Black = 1, White = 2
Coordinates (1,3) is first row down, 3rd column over

Root.move is move that opponent made to get to current spot, so root.move is "None"
root.children = moves available for ai to make
root.value holds board_pts value keys matched with corresponding children from root.children that would result in that value
Leaves with value == None probably pruned
'''
debug = False

search_depth = 6# Search depth for recursive func


class Tree():
    def __init__(self, color, move=None):
        self.color = color
        self.move = move
        self.value = None
        self.children = []
        self.alpha = -999
        self.beta = 999


def color(color: int):
    return "B" if color == 1 else "W"


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
        self.dif_val = False

    def get_move(self, move):
        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])  # Run opponent's move for self.board
        else:
            self.color = 1

        root = Tree(self.opponent[self.color])  # Tree root
        self.rec_tree(root, search_depth)  # Set up tree

        self.rec_min_max_heuristic(root)

        #self.rec_abp_heuristic(root)

        #self.rec_abp_v2(root)


        avail_moves = root.value[list(root.value)[0]]

        #cur_move = avail_moves[randint(0,len(avail_moves)-1)]
        cur_move = avail_moves[0]

        '''
        print("ALL MOVES")
        moves = self.board.get_all_possible_moves(self.color)
        for i, checker_moves in enumerate(moves):
            print(i, ':[', end="")
            for j, move in enumerate(checker_moves):
                print(j, ":", move, end=", ")
            print("]")
        print("AVAIL MOVES")
        #print(avail_moves)
        for i, checker_moves in enumerate(avail_moves):
            print(i, ':[', end="")
            for j, move in enumerate(checker_moves):
                print(j, ":", move, end=", ")
            print("]")
        '''
        #if self.dif_val:
        if debug: print("##########TREE##########")
        self.print_tree(root)
        if debug: print("##########TREE##########")
#            self.dif_val = False
        self.board.make_move(cur_move, self.color)  # Make the optimal move
        move = cur_move
        return move

    # Board Heuristic
    def board_points(self):  # 5 + row number for pawns, 5 + row number + 2 for kings
        king_pts_value = 5 + (self.row - 1) + 2 #5 pts for piece, self.row -1 pts for pts at end of board, + 1 for being king

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
                    #pts -= (11 - checker.row)  # 5 + (6 - Row)
                    if checker.is_king:
                        pts -= king_pts_value
                    else:
                        pts -= (5 + (self.row - checker.row - 1)) #5 + (Num of rows - Row - 1) eg. 5x5 board, 5th row is 5(num) - 4(row) -1 = 0

        if abs(pts) > 2:
            self.dif_val = True
        #if debug: print(color(root.color), pts, -pts)
        return pts if self.color == 2 else -pts #BLACK(1) GOES FIRST, so positive points, if self.color == white(2), then return white pieces as positive points

    def print_tree(self, root, level=0):
        if not debug:
            return
        print("\t" * level, color(root.color), root.value, "->", root.move)
        if len(root.children) != 0:  # Not Leaf node
            for child in root.children:
                self.print_tree(child, level + 1)

    def rec_tree(self, root: Tree, level=1):  # Create tree up to depth level
        if level == 0:
            pass
        else:
            if root.move is not None:  # Not root of tree
                self.board.make_move(root.move, root.color)
            # Check if win here maybe?
            avail_moves = self.board.get_all_possible_moves(self.opponent[root.color])
            for i in range(len(avail_moves)):
                for j in range(len(avail_moves[i])):
                    # print(root)
                    root.children.append(Tree(self.opponent[root.color], avail_moves[i][j]))
            for child in root.children:
                self.rec_tree(child, level - 1)

            if root.move is not None:
                self.board.undo()

    # MinMax Functions
    def ftu(self, color):  # Function to use (min vs max by color)
        if color == self.color:  # Calculate Max
            return max
        else:  # Calculate Min
            return min

    def min_max(self, children, color):  # Returns dict -> {Max/min value: Moves to get here}
        ftu = self.ftu(color)  # Use corresponding min or max depending on color
        value_map = {}
        for child in children:
            for v in child.value.keys():
                value_map.setdefault(v, []).append(child.move)  # D: {heuristic value: Move to make to get here}
        # print(value_map)
        return {ftu(value_map): value_map[ftu(value_map)]}

    def rec_min_max_heuristic(self, root: Tree):  # Apply min_max heuristic to tree
        if root.move is not None:  # AKA this is root, the move is what opponent made to get here (none so we don't have to redo move on our board)
            self.board.make_move(root.move, root.color)
        if len(root.children) == 0:  # Passed node has no children
            # Evaluate heuristic for board(and return?)
            root.value = {
                self.board_points(): []}  # Value will be dict with key = heuristic points and value = all the moves that result in that many points
        else:  # Evaluate rec_heuristic for children, then retrieve values and apply min/max as appropriate
            for child in root.children:
                self.rec_min_max_heuristic(child)
            root.value = self.min_max(root.children, root.color)

        if root.move is not None:
            self.board.undo()  # Undo move to revert action (done for searching) and return to parent

    # AlphaBeta Functions
    def set_alpha_beta(self, root, child, color):
        ftu = self.ftu(color)
        if child.value is None:
            print(child)
        if root.value is None:
            root.value = {}
        if color == self.color:  # Max aka update alpha (This ai's turn)
            # return ftu(alpha, ftu(child.value)), beta
            if root.alpha < ftu(child.value):
                root.alpha = ftu(child.value)
            root.value.setdefault(root.alpha, []).append(child.move)
        else:  # Min aka update beta (Opponent's turn)
            # return alpha, ftu(beta, ftu(child.value))
            if root.beta > ftu(child.value):
                root.beta = ftu(child.value)
            root.value.setdefault(root.beta, []).append(child.move)

    def rec_abp_heuristic(self, root: Tree, alpha=-999, beta=999, level = 0):  # Alpha Beta Pruning
        if debug: print("\t" * level, color(root.color), "Enter: ", root.value, "->", root.move)
        old_val = root.value
        if root.move is not None:  # AKA this is root, the move is what opponent made to get here (none so we don't have to redo move on our board)
            self.board.make_move(root.move, root.color)
        #self.board.show_board()
        if len(root.children) == 0:  # Passed node has no children aka this is lowest level/leaf
            root.value = {self.board_points(): []}
            if debug: print("\t" * level, "LEAF: ", root.value, "->", root.move)
        else:  # Evaluate heuristic for child, retrieve value, update alphabeta, continue with next child if appropriate
            root.alpha = alpha
            root.beta = beta

            if debug: print("\t" * 16, "CHILDREN:", end=" ")
            for child in root.children:
                if debug: print(child.move, end=", ")
            if debug: print("(",color(self.opponent[root.color]), ")", sep="")

            for child in root.children:
                if root.alpha >= root.beta:  # Break out of loop once alpha >= beta (Pruning)
                    if debug: print("PRUNING")
                    break
                self.rec_abp_heuristic(child, root.alpha, root.beta, level + 1)
                self.set_alpha_beta(root, child, root.color)  # Apply alpha/beta values based on min/max of child to current node
                if debug: print("\t" * level, color(root.color), "New Value: ", root.value, "->", root.move)
        if root.move is not None:
            self.board.undo()
        if debug: print("\t" * level, color(root.color), "Exit: ", root.value, "->", root.move)
        #print(max(list(root.value), key = abs), "\t", root.move, "->", root.value)
        #if abs(max(list(root.value), key = abs)) > 2:
            #print("\t" * level, "Enter: ", old_val, "->", root.move)
            #print("\t" * level, "Exit: ", root.value, "->", root.move)

    def rec_abp_v2(self, root: Tree, alpha = -999, beta = 999):
        if root.move is not None:  # AKA this is root, the move is what opponent made to get here (none so we don't have to redo move on our board)
            self.board.make_move(root.move, root.color)
        else:
            root.value = {}
        if len(root.children) == 0:
            root.value = self.board_points()
            if root.move is not None:
                self.board.undo()
            return root.value
        else:
            if color == self.color: #MaximizingPlayer
                #val = -999
                for child in root.children:
                    '''
                    val = max(val, rec_abp_v2(child, alpha, beta))
                    alpha = max(alpha, val)
                    '''
                    val = self.rec_abp_v2(child, alpha, beta)
                    if alpha > val: #Alpha > Val
                        root.alpha = alpha
                    else: #Val > Alpha
                        alpha = val
                        if root.move is None: #Root node, ie save the move to get here
                            root.value.setdefault(alpha, []).append(child.move)
                        root.alpha = alpha
                    if alpha >= beta:
                        break
                if root.move is not None:
                    self.board.undo()
                return alpha
            else: #Minimizing Player
                #val = 999
                for child in root.children:
                    '''
                    val = min(val, alphabeta(child, alpha, beta))
                    beta = min(val, beta)
                    '''
                    val = self.rec_abp_v2(child, alpha, beta)
                    if beta < val: #Beta < Val
                        root.beta = beta
                    else:
                        beta = val
                        if root.move is None:
                            root.value.setdefault(beta, []).append(child.move)
                        root.beta = beta
                    if alpha >= beta:
                        break
                if root.move is not None:
                    self.board.undo()
                return beta


