import pandas as pd
import json
import heapq
import time
from tqdm import tqdm

def load_data(file_path):
    return pd.read_csv(file_path)

def parse_puzzle_status(puzzles_df, puzzle_info_df):
    puzzles_df['parsed_initial_state'] = puzzles_df['initial_state'].apply(lambda x: x.split(';'))
    puzzles_df['parsed_solution_state'] = puzzles_df['solution_state'].apply(lambda x: x.split(';'))
    puzzle_info_df['allowed_moves'] = puzzle_info_df['allowed_moves'].apply(lambda x: json.loads(x.replace("'", '"')))
    return puzzles_df, puzzle_info_df

def apply_move(state, move, inverse=False):
    if inverse:
        inverse_move = {v: k for k, v in enumerate(move)}
        return [state[inverse_move[i]] for i in range(len(state))]
    else:
        return [state[i] for i in move]

def a_star_search_with_timeout(initial_state, goal_state, allowed_moves, timeout=300):
    start_time = time.time()
    open_set = []
    heapq.heappush(open_set, (0, initial_state, []))
    closed_set = set()

    while open_set:
        if time.time() - start_time > timeout:
            return None

        _, current_state, path = heapq.heappop(open_set)

        if current_state == goal_state:
            return path

        state_tuple = tuple(current_state)
        if state_tuple in closed_set:
            continue

        closed_set.add(state_tuple)

        for move_name, move in allowed_moves.items():
            for inverse in [False, True]:
                new_state = apply_move(current_state, move, inverse)
                new_state_tuple = tuple(new_state)
                if new_state_tuple not in closed_set:
                    priority = len(path) + 1 + heuristic(new_state, goal_state)
                    heapq.heappush(open_set, (priority, new_state, path + [(move_name, inverse)]))

def heuristic(state, goal_state):
    return sum(s != g for s, g in zip(state, goal_state))

def improved_heuristic_with_wildcards(state, goal_state, num_wildcards):
    mismatches = sum(s != g for s, g in zip(state, goal_state))
    return max(0, mismatches - num_wildcards)

def improved_a_star_search_with_wildcards(initial_state, goal_state, allowed_moves, num_wildcards, max_depth=30, timeout=100):
    start_time = time.time()
    open_set = []
    heapq.heappush(open_set, (0, initial_state, [], num_wildcards))
    closed_set = set()

    while open_set:
        if time.time() - start_time > timeout:
            return None

        _, current_state, path, remaining_wildcards = heapq.heappop(open_set)

        if len(path) > max_depth:
            continue

        if current_state == goal_state or improved_heuristic_with_wildcards(current_state, goal_state, remaining_wildcards) == 0:
            return path

        closed_set.add((tuple(current_state), remaining_wildcards))

        for move_name, move in allowed_moves.items():
            for inverse in [False, True]:
                new_state = apply_move(current_state, move, inverse)
                if (tuple(new_state), remaining_wildcards) not in closed_set:
                    priority = len(path) + 1 + improved_heuristic_with_wildcards(new_state, goal_state, remaining_wildcards)
                    heapq.heappush(open_set, (priority, new_state, path + [(move_name, inverse)], remaining_wildcards))

def format_solution_for_submission(puzzle_id, solution_moves):
    formatted_moves = []
    for move, inverse in solution_moves:
        move_str = '-' + move if inverse else move
        formatted_moves.append(move_str)

    return {'id': puzzle_id, 'moves': '.'.join(formatted_moves)}

def solve_puzzles(puzzles_df, puzzle_info_df, sample_submission_df, num_puzzles=None, limit_index=30):
    solutions = []

    puzzles_to_solve = puzzles_df if num_puzzles is None else puzzles_df.head(num_puzzles)

    for index, row in tqdm(puzzles_to_solve.iterrows(), total=puzzles_to_solve.shape[0], desc="Solving Puzzles"):
        puzzle_id = row['id']
        initial_state = row['parsed_initial_state']
        goal_state = row['parsed_solution_state']
        puzzle_type = row['puzzle_type']
        num_wildcards = row['num_wildcards']
        allowed_moves = puzzle_info_df[puzzle_info_df['puzzle_type'] == puzzle_type]['allowed_moves'].iloc[0]
        
        solution_moves = None
        
        if index < limit_index:
            solution_moves = improved_a_star_search_with_wildcards(initial_state, goal_state, allowed_moves, num_wildcards)

        if solution_moves is None:
            solution_moves = sample_submission_df[sample_submission_df['id'] == puzzle_id]['moves'].iloc[0].split('.')
            solution_moves = [(move.replace('-', ''), move.startswith('-')) for move in solution_moves]

        formatted_solution = format_solution_for_submission(puzzle_id, solution_moves)
        solutions.append(formatted_solution)
        #print(formatted_solution)
    return pd.DataFrame(solutions)

if __name__ == "__main__":
    # File paths
    puzzle_info_path = 'puzzle_info.csv'
    puzzles_path = 'puzzles.csv'
    sample_submission_path = 'sample_submission.csv'

    # Loading the data
    puzzle_info_df = load_data(puzzle_info_path)
    puzzles_df = load_data(puzzles_path)
    sample_submission_df = load_data(sample_submission_path)

    # Parse puzzle status
    puzzles_df, puzzle_info_df = parse_puzzle_status(puzzles_df, puzzle_info_df)

    # Solve puzzles
    solved_puzzles_df = solve_puzzles(puzzles_df, puzzle_info_df, sample_submission_df, num_puzzles=None, limit_index=398)

    # Save submission
    submission_csv_path = 'submission.csv'
    solved_puzzles_df.to_csv(submission_csv_path, index=False)