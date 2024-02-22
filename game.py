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
    puzzle=Sudoku(puzzle_size,board=puzzle_board)
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
    initial_state = puzzle.board
    puzzle_size = len(initial_state) 
    
    if test_goal(initial_state, puzzle):
        return initial_state

    frontier = queue.Queue()
    frontier.put(initial_state)
    explored = set()

    while not frontier.empty():
        state = frontier.get()
        state_tup = tuple(map(tuple, state))
        if state_tup in explored:
            continue

        explored.add(state_tup)

        for cell in empty_cells(state):
            for value in range(1, puzzle_size**2 + 1):  
                new_state = copy.deepcopy(state)
                new_state[cell[0]][cell[1]] = value
                new_state_tup = tuple(map(tuple, new_state))

                
                if new_state_tup not in explored:
                    if test_goal(new_state, puzzle):
                        return new_state
                    frontier.put(new_state)
                    explored.add(new_state_tup)

    return None

'''
params: Takes the current puzzle as input
Return: The puzzle board corresponding to the goal
Note: You can modify the function definition as you see fit
'''
def dfs(puzzle):
    #Write Code here
    initial_state = puzzle.board
    puzzle_size = len(initial_state)

    if test_goal(initial_state, puzzle):
        return initial_state

    frontier = []
    frontier.append(initial_state)
    explored = set()

    while frontier:
        state = frontier.pop()
        state_tup = tuple(map(tuple, state))
        if state_tup in explored:
            continue

        explored.add(state_tup)

        for cell in empty_cells(state):
            for value in range(1, puzzle_size**2 + 1):
                new_state = copy.deepcopy(state)
                new_state[cell[0]][cell[1]] = value
                new_state_tup = tuple(map(tuple, new_state))

                if new_state_tup not in explored:
                    if test_goal(new_state, puzzle):
                        return new_state
                    frontier.append(new_state)
    return None

'''
params: Takes the current puzzle as input
Return: The puzzle board corresponding to the goal
Note: You can modify the function definition as you see fit
'''
def bfs_with_prunning(puzzle):
    initial_state = puzzle.board
    puzzle_size = len(initial_state)

    if test_goal(initial_state, puzzle):
        return initial_state

    frontier = queue.Queue()
    frontier.put(initial_state)
    explored = set()

    while not frontier.empty():
        state = frontier.get()
        state_tup = tuple(map(tuple, state))
        if state_tup in explored:
            continue

        explored.add(state_tup)

        for cell in empty_cells(state):
            for value in range(1, puzzle_size**2 + 1):
                new_state = copy.deepcopy(state)
                new_state[cell[0]][cell[1]] = value
                new_state_tup = tuple(map(tuple, new_state))

                if new_state_tup not in explored:
                    if valid_puzzle(puzzle_size, new_state):
                        explored.add(new_state_tup)  # Mark this new state as explored
                        if test_goal(new_state, puzzle):
                            return new_state
                        frontier.put(new_state)

    #Write Code here
    return None

'''
params: Takes the current puzzle as input
Return: The puzzle board corresponding to the goal
Note: You can modify the function definition as you see fit
'''
def dfs_with_prunning(puzzle):
    #Write Code here
    initial_state = puzzle.board
    puzzle_size = len(initial_state)

    if test_goal(initial_state, puzzle):
        return initial_state

    frontier = []
    frontier.append(initial_state)
    explored = set()

    while frontier:
        state = frontier.pop()
        state_tup = tuple(map(tuple, state))
        if state_tup in explored:
            continue

        explored.add(state_tup)

        for cell in empty_cells(state):
            for value in range(1, puzzle_size**2 + 1):
                new_state = copy.deepcopy(state)
                new_state[cell[0]][cell[1]] = value
                new_state_tup = tuple(map(tuple, new_state))

                if new_state_tup not in explored and valid_puzzle(puzzle_size, new_state):
                    if test_goal(new_state, puzzle):
                        return new_state
                    frontier.append(new_state)
                    explored.add(new_state_tup)
    return None


if __name__ == "__main__":
    puzzle = Sudoku(2,2).difficulty(0.2)  # Constructs a 2 x 2 puzzle
    puzzle.show()  # Pretty prints the puzzle
    print(valid_puzzle(2, puzzle.board))  # Checks if the puzzle is valid
    print(test_goal(puzzle.board, puzzle))  # Checks if the given puzzle board is the goal for the puzzle
    print(empty_cells(puzzle.board))  # Prints the empty cells as row and column values in a list for the current puzzle board

    def dynamic_wrapper(func, size, difficulty):
        def wrapped():
            puzzle = Sudoku(size, size).difficulty(difficulty)
            return func(puzzle)
        return wrapped

    for size in [2, 4]:
        for difficulty in [0.2, 0.4, 0.6, 0.8]:
            wrapped_bfs = dynamic_wrapper(bfs, size, difficulty)
            runtime = timeit.timeit(wrapped_bfs, number=1)
            print(f"bfs: {runtime} seconds")
    wrapped_bfs_with_prunning = dynamic_wrapper(bfs_with_prunning, 2, 0.2)
    runtime = timeit.timeit(wrapped_bfs_with_prunning, number=1)
    print(f"bfs_with_prunning: {runtime} seconds")