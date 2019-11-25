from BoardClasses import Board

# The following part should be completed by students.
# Students can modify anything except the class name and exisiting functions and varibles.
search_depth = 5  # Search depth for recursive func


class Tree():
    def __init__(self, color, move=None):
        self.color = color
        self.move = move
        self.value = None
        self.children = []
        self.alpha = -999
        self.beta = 999


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

        root = Tree(self.opponent[self.color])  # Tree root
        self.rec_tree(root, search_depth)  # Set up tree
        #self.rec_min_max_heuristic(root)
        self.rec_abp_heuristic(root)

        avail_moves = root.value[list(root.value)[0]]
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

        self.board.make_move(cur_move, self.color)  # Make the optimal move
        move = cur_move
        return move

    # Board Heuristic
    def board_points(self):  # 5 + row number for pawns, 5 + row number + 2 for kings
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
        return pts if self.color == "B" else -pts

    def print_tree(self, root, level=0):
        # print("PRINTING TREE")

        print("\t" * level, root.value, "->", root.move)
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
        else:  # Calculate Max
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
        if color == self.color:  # Max aka update alpha
            # return ftu(alpha, ftu(child.value)), beta
            if root.alpha < ftu(child.value):
                root.alpha = ftu(child.value)
            root.value.setdefault(root.alpha, []).append(child.move)
        else:  # Min aka update beta
            # return alpha, ftu(beta, ftu(child.value))
            if root.beta > ftu(child.value):
                root.beta = ftu(child.value)
            root.value.setdefault(root.beta, []).append(child.move)

    def rec_abp_heuristic(self, root: Tree, alpha=-999, beta=999):  # Alpha Beta Pruning
        if root.move is not None:  # AKA this is root, the move is what opponent made to get here (none so we don't have to redo move on our board)
            self.board.make_move(root.move, root.color)
        if len(root.children) == 0:  # Passed node has no children aka this is lowest level/leaf
            root.value = {self.board_points(): []}
        else:  # Evaluate heuristic for child, retrieve value, update alphabeta, continue with next child if appropriate
            root.alpha = alpha
            root.beta = beta
            for child in root.children:
                if root.alpha >= root.beta:  # Break out of loop once alpha >= beta (Pruning)
                    break
                self.rec_abp_heuristic(child, root.alpha, root.beta)
                self.set_alpha_beta(root, child, root.color)  # Apply alpha/beta values based on min/max of child to current node
        if root.move is not None:
            self.board.undo()
