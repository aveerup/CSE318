import heapq;

class node:

    def __init__(self, board, priority, prev_node, moves_so_far):
        self.board = board;
        self.priority = priority;
        self.prev_node = prev_node;
        self.moves_so_far = moves_so_far;

    def __lt__(self, other):
        return self.priority <= other.priority;

    def __eq__(self, other):
        return self.board == other.board and self.priority == other.priority and self.prev_node == other.prev_node;

    def __str__(self):
        return f"board: {self.board} \nMinimum number of moves = {self.moves_so_far}";

def even(number):
    if number & 1:
        return False;
    else:
        return True;

def Hamming_distance(board):
    n = len(board[0]);

    hamming_distance = 0;
    for i in range(n):
        for j in range(n):
            if n*i+j+1 != board[i][j] and board[i][j] != 0:
                hamming_distance += 1;

    return hamming_distance;

def Manhattan_distance(board):
    n = len(board[0]);

    manhattan_distance = 0;
    for i in range(n):
        for j in range(n):
            if board[i][j] != 0:
                row = (board[i][j] - 1)//3
                col = (board[i][j] - 1)%3
            else:
                continue;
            
            manhattan_distance += abs(row - i)
            manhattan_distance += abs(col - j)

    # print("manhattan distance : ",manhattan_distance);
    return manhattan_distance;

def Euclidean_distance(board):
    n = len(board[0]);

    euclidean_distance = 0;
    for i in range(n):
        for j in range(n):
            if board[i][j] != 0:
                row = (board[i][j] - 1)//3
                col = (board[i][j] - 1)%3

                euclidean_distance += ((row - i)**2 + (col - j)**2)**0.5;

    return euclidean_distance;

def Linear_conflict_helper(board, dest_row, dest_col, curr_row, curr_col):
    n = len(board[0]);
    conflicts = 0;

    if dest_row[curr_row][curr_col] == curr_row:
        for i in range(curr_col +1, n):
            if dest_row[curr_row][i] == curr_row:
                if dest_col[curr_row][curr_col] > dest_col[curr_row][i]:
                    conflicts += 1;

    if dest_col[curr_row][curr_col] == curr_col:
        for i in range(curr_row +1, n):
            if dest_col[i][curr_col] == curr_col:
                if dest_row[curr_row][curr_col] > dest_row[i][curr_col]:
                    conflicts += 1;

    return conflicts;


def Linear_conflict(board):
    n = len(board[0]);

    # print("board ", board);

    dest_row = [[y for y in x] for x in board]
    dest_col = [[y for y in x] for x in board]

    # print("dest_row ", dest_row);

    for i in range(n):
        for j in range(n):
            if board[i][j] == 0:
                dest_row[i][j] = n - 1;
                dest_col[i][j] = n - 1;
            else:
                dest_row[i][j] = (board[i][j] -1)//n;
                dest_col[i][j] = (board[i][j] -1)%n;

    conflicts = 0;
    for i in range(n):
        for j in range(n):
            conflicts += Linear_conflict_helper(board, dest_row, dest_col, i, j);
    
    # print("conflicts ", conflicts);
            
    return Manhattan_distance(board) + 2*conflicts;

def priority_func(board, g_n):
    return g_n + Linear_conflict(board);


def inversion(sequence, left, right):
    # print("left ", left, " right ", right);
    # print(sequence)
    if left == right:
        return 0;

    mid = left + (right - left)//2;

    left_sequence = sequence[ : mid+1]
    right_sequence = sequence[mid + 1 : right+1]

    inversion_no = 0;
    inversion_no += inversion(left_sequence, 0, mid - left);
    inversion_no += inversion(right_sequence, 0, right - mid - 1);

    i = 0;
    j = 0;
    sequence = [];
    while i < mid-left+1 and j < right-mid:
        if left_sequence[i] < right_sequence[j]:
            sequence.append(left_sequence[i]);
            i += 1;
        else:
            # code to find out the inversions in the board
            # t = i;
            # while t < mid-left+1:
            #     print(left_sequence[t], " ", right_sequence[j]);
            #     t += 1;
            inversion_no += (mid - left) - i +1;
            sequence.append(right_sequence[j]);
            j += 1;

    while i < mid-left+1:
        sequence.append(left_sequence[i]);
        i += 1;

    while j < right-mid:
        sequence.append(right_sequence[j]);
        j += 1;

    return inversion_no;


def solvable(n, board):

    board_sequence = [];
    blank_row = 0;
    for i in range(n):
        for j in range(n):
            if board[i][j] == 0:
                blank_row = n - i;
                continue;
             
            board_sequence.append(board[i][j]);
             

    inversion_no = inversion(board_sequence, 0, len(board_sequence)-1);
    print("inversion_no ", inversion_no);
    if even(n):
        if (even(blank_row) and not even(inversion_no)) or (not even(blank_row) and even(inversion_no)):
            return True;
    else:
        if even(inversion_no):
            return True;

    return False;


def goal_board(board):
    n = len(board[0])

    for i in range(n):
        for j in range(n):
            if board[i][j] != n*i + j + 1 and board[i][j] != 0:
                return False;

    return True;


def solve(open_list):
    explored = 1;
    expanded = 0;

    while len(open_list) != 0:
        least_priority_node = heapq.heappop(open_list);
        expanded += 1;
        # print("current board ", least_priority_node.board);
        # print("current priority ", least_priority_node.priority);

        if goal_board(least_priority_node.board):
            return least_priority_node, explored, expanded;

        closed_list.append(least_priority_node)

        n = len(least_priority_node.board[0])
        blank_row = 0;
        blank_col = 0;

        for i in range(n):
            for j in range(n):
                if least_priority_node.board[i][j] == 0:
                    blank_row = i;
                    blank_col = j;

        if 0 <= blank_row - 1:
            up_move_board = [row[:] for row in least_priority_node.board];
            up_move_board[blank_row ][blank_col] = up_move_board[blank_row -1][blank_col];
            up_move_board[blank_row -1][blank_col] = 0; 
            
            new_node = node(up_move_board, priority_func(up_move_board, least_priority_node.moves_so_far + 1), least_priority_node, least_priority_node.moves_so_far + 1);
            if new_node not in open_list:
                heapq.heappush(open_list, new_node);
                explored += 1;

        if blank_row + 1 < n:
            down_move_board = [row[:] for row in least_priority_node.board];
            down_move_board[blank_row][blank_col] = down_move_board[blank_row + 1][blank_col];
            down_move_board[blank_row + 1][blank_col] = 0; 
            
            new_node = node(down_move_board, priority_func(down_move_board, least_priority_node.moves_so_far + 1), least_priority_node, least_priority_node.moves_so_far + 1);
            if new_node not in open_list:
                heapq.heappush(open_list, new_node);
                explored += 1;
        
        if 0 <= blank_col - 1:
            left_move_board = [row[:] for row in least_priority_node.board];
            left_move_board[blank_row ][blank_col] = left_move_board[blank_row][blank_col - 1];
            left_move_board[blank_row][blank_col - 1] = 0; 
            
            new_node = node(left_move_board, priority_func(left_move_board, least_priority_node.moves_so_far + 1), least_priority_node, least_priority_node.moves_so_far + 1);
            if new_node not in open_list:
                heapq.heappush(open_list, new_node);
                explored += 1;

        if blank_col + 1 < n:
            right_move_board = [row[:] for row in least_priority_node.board];
            right_move_board[blank_row ][blank_col] = right_move_board[blank_row][blank_col + 1];
            right_move_board[blank_row][blank_col + 1] = 0; 
            
            new_node = node(right_move_board, priority_func(right_move_board, least_priority_node.moves_so_far + 1), least_priority_node, least_priority_node.moves_so_far + 1);
            if new_node not in open_list:
                heapq.heappush(open_list, new_node);
                explored += 1;


def print_step(final_node):

    if final_node.prev_node is None:
        for row in final_node.board:
            for col in row:
                print(col, end=" ");
            print("");
        print("")

        return ;

    print_step(final_node.prev_node);
    for row in final_node.board:
            for col in row:
                print(col, end=" ");
            print("");
    print("");

    return;
        


n = int(input())

board = []
for _ in range(n):
    row = list(map(int, input().split()))
    board.append(row)

closed_list = []
open_list = []
explored = 0;
expanded = 0;
if solvable(n, board):
    initial_node = node(board, priority_func(board, 0), None, 0);
    open_list.append(initial_node);
    explored += 1;

    final_node, explored, expanded = solve(open_list);

    print(final_node, "\nexplored node : ", explored, "\nexpanded node : ", expanded, "\n");
    print_step(final_node);
else:
    print("Board not solvable");



# In general, for a given grid of width N, we can find out check if a N*N – 1 puzzle is solvable or not by following below simple rules : 
 
# If N is odd, 
# then puzzle instance is solvable if number of inversions is even in the input state.

# If N is even, 
# puzzle instance is solvable if 
# > the blank is on an even row counting from the bottom (second-last, fourth-last, etc.) 
# and number of inversions is odd.
# > the blank is on an odd row counting from the bottom (last, third-last, fifth-last, etc.) 
# and number of inversions is even.
# For all other cases, the puzzle instance is not solvable.
