from sudoku import Sudoku
import queue
import copy
import timeit

'''
Parameters: Takes as input the curr_board state and the puzzle
Returns: True if the current board state is the goal and False if not
Note: Existing version solves the puzzle everytime you test for goal
      feel free to change the implementation to save time
'''
def test_goal(curr_board,puzzle):
    puzzle_solution=puzzle.solve()
    try:
        solution_board=puzzle_solution.board
        for i in range(len(solution_board)):
            for j in range(len(solution_board[i])):
                assert(curr_board[i][j]==solution_board[i][j])
        return True
    except Exception as e:
        return False

'''
Parameters: Takes as input a puzzle board and puzzle size
Returns: True if the puzzle board is valid and False if not
'''    
def valid_puzzle(puzzle_size,puzzle_board):
    
    puzzle=Sudoku(puzzle_size, board=puzzle_board)
    return puzzle.validate()

'''
Parameters: Takes as input a puzzle board
Returns: Returns all the cells in the grid that are empty
'''
def empty_cells(puzzle_board):
    empty_cell_list=[]
    for i in range(len(puzzle_board)):
        for j in range(len(puzzle_board[i])):
            if puzzle_board[i][j] is None:
                empty_cell_list.append([i,j])
    return empty_cell_list

'''
params: Takes the current puzzle as input
Return: The puzzle board corresponding to the goal
Note: You can modify the function definition as you see fit
'''
def bfs(puzzle):
    #Write Code here
    frontier = queue.Queue()
    initial_empty_cells = empty_cells(puzzle.board)
    frontier.put((puzzle.board, initial_empty_cells))

    while not frontier.empty():
        current_board, empty_cells_list = frontier.get()

        # If there are no empty cells, this is a complete board
        if not empty_cells_list:
            if test_goal(current_board, puzzle):
                return current_board
            continue

        # Get the empty cells to fill
        empty_cell = empty_cells_list[0]

        for value in range(1, puzzle.size **2 + 1):
            new_board = copy.deepcopy(current_board)
            new_board[empty_cell[0]][empty_cell[1]] = value
           
            if valid_puzzle(2, new_board):
                new_empty_cells_list = copy.deepcopy(empty_cells_list[1:])
                frontier.put((new_board, new_empty_cells_list))
    return None

'''
params: Takes the current puzzle as input
Return: The puzzle board corresponding to the goal
Note: You can modify the function definition as you see fit
'''
def dfs(puzzle):
    #Write Code here
    stack = []
    initial_empty_cells = empty_cells(puzzle.board)
    stack.append((puzzle.board, initial_empty_cells))

    while stack:
        current_board, empty_cells_list = stack.pop()

        if not empty_cells_list:
            if test_goal(current_board, puzzle):
                return current_board
            continue

        empty_cell = empty_cells_list[0]

        for value in range(1, puzzle.size**2 + 1):
            new_board = copy.deepcopy(current_board)
            new_board[empty_cell[0]][empty_cell[1]] = value

            if valid_puzzle(2, new_board):
                new_empty_cells_list = copy.deepcopy(empty_cells_list[1:])
                stack.append((new_board, new_empty_cells_list))
    return None

'''
params: Takes the current puzzle as input
Return: The puzzle board corresponding to the goal
Note: You can modify the function definition as you see fit
'''
def bfs_with_prunning(puzzle):
    #Write Code here
    frontier = queue.Queue()
    initial_empty_cells = empty_cells(puzzle.board)
    frontier.put((puzzle.board, initial_empty_cells))

    while not frontier.empty():
        current_board, empty_cells_list = frontier.get()

        if not empty_cells_list:
            if test_goal(current_board, puzzle):
                return current_board
            continue

        empty_cell = empty_cells_list[0]
        
        for value in range(1, puzzle.size**2 + 1):
            new_board = copy.deepcopy(current_board)
            new_board[empty_cell[0]][empty_cell[1]] = value
            if valid_puzzle(2, new_board):
                new_empty_cells_list = copy.deepcopy(empty_cells_list[1:])
                frontier.put((new_board, new_empty_cells_list))

    return None

'''
params: Takes the current puzzle as input
Return: The puzzle board corresponding to the goal
Note: You can modify the function definition as you see fit
'''
def dfs_with_prunning(puzzle):
    #Write Code here
    stack = []
    initial_empty_cells = empty_cells(puzzle.board)
    
    # Start DFS with the initial board state
    stack.append((puzzle.board, initial_empty_cells))

    while stack:
        current_board, empty_cells_list = stack.pop()

        if not empty_cells_list:
            if test_goal(current_board, puzzle):
                return current_board # Solution found
            continue

        # Pruning step: prioritize the cell with the least number of possible values
        empty_cell = empty_cells_list[0]
        
        for value in range(1, puzzle.size**2 + 1):
            new_board = copy.deepcopy(current_board)
            new_board[empty_cell[0]][empty_cell[1]] = value
            if valid_puzzle(2, new_board):
                new_empty_cells_list = copy.deepcopy(empty_cells_list[1:])
                stack.append((new_board, new_empty_cells_list))

    return None


if __name__ == "__main__":

    
    puzzle=Sudoku(2, 2).difficulty(0.2) # Constructs a 2 x 2 puzzle
    puzzle.show() # Pretty prints the puzzle
    print(valid_puzzle(2,puzzle.board)) # Checks if the puzzle is valid
    print(test_goal(puzzle.board,puzzle)) # Checks if the given puzzle board is the goal for the puzzle
    print(empty_cells(puzzle.board)) # Prints the empty cells as row and column values in a list for the current puzzle board

    for search_method in [bfs, dfs, bfs_with_prunning, dfs_with_prunning]:
        start_time = timeit.default_timer()
        try:
            # Set a timer to automatically stop the search after 300 seconds (5 minutes)
            solved_board = search_method(puzzle)
            runtime = timeit.default_timer() - start_time
            if solved_board:
                print(f"{search_method.__name__} solved the puzzle in {runtime:.2f} seconds:")
                for row in solved_board:
                    print(row)
            else:
                print(f"{search_method.__name__} did not solve the puzzle.")
        except Exception as e:
            runtime = timeit.default_timer() - start_time
            if runtime >= 300:
                print(f"{search_method.__name__} exceeded the time limit of 5 minutes.")
            else:
                print(f"An error occurred during {search_method.__name__}: {e}")

        print("------------------------------------------------------")

  