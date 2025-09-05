# Santa 2023 - Polytope Permutation Puzzle

This project is based on the [Santa 2023 Kaggle Competition](https://www.kaggle.com/competitions/santa-2023/overview). The challenge is to find the shortest sequence of moves to transform an initial permutation into a goal permutation using a set of allowed moves.

## Competition Overview

Santa's Polytope Permutation Puzzle is a combinatorial optimization problem. The objective is to solve a series of puzzles by finding the minimal sequence of moves (permutations) that transforms a given start state into a target state. Each move is defined by a set of allowed permutations.

For more details, see the [Kaggle competition page](https://www.kaggle.com/competitions/santa-2023/overview).

## Features

- AI-driven logic for solving permutation puzzles
- Example algorithms and code for educational and research purposes
- Modular and extensible codebase

## Requirements

- Python 3.8 or higher
- pandas
- numpy
- tqdm

Install dependencies with:

```bash
pip install -r requirements.txt
```

or manually:

```bash
pip install pandas numpy tqdm
```

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/santa.git
   ```
2. **Navigate to the project directory:**
   ```bash
   cd "d:\My files\NJCU\Spring 2024\CS4041299 Artificial Intelligence\Santa\santa"
   ```
3. **Install dependencies:**  
   See the Requirements section above.

4. **Run the application:**
   ```bash
   python main.py
   ```
   _(Replace `main.py` with your entry script if different.)_

## Usage

- Download sample puzzles and data from the [Kaggle competition data page](https://www.kaggle.com/competitions/santa-2023/data).
- Place the data files in the project directory.
- Run the main script to solve puzzles and generate a submission file.
- Example:
  ```bash
  python main.py --input puzzles.csv --output submission.csv
  ```
- For more options, see the script's help:
  ```bash
  python main.py --help
  ```

## Code Structure

This project provides code to solve the Santa Polytope Permutation Puzzle by finding the shortest sequence of moves from an initial state to a goal state using allowed moves. Below is a summary of the main functions:

- **load_data(file_path):** Loads data from a CSV file into a Pandas DataFrame, including puzzle information, states, and sample submissions.
- **parse_puzzle_status(puzzles_df, puzzle_info_df):** Parses puzzle status, splits initial and solution states, and converts allowed moves from JSON to Python objects.
- **apply_move(state, move, inverse=False):** Applies a move to a given state, simulating the effect of a move.
- **a_star_search_with_timeout(initial_state, goal_state, allowed_moves, timeout=300):** Performs A\* search with a timeout to find the shortest sequence of moves.
- **heuristic(state, goal_state):** Computes the heuristic value between a state and the goal state for A\* search.
- **improved_heuristic_with_wildcards(state, goal_state, num_wildcards):** Computes an improved heuristic considering wildcard elements in the state.
- **improved_a_star_search_with_wildcards(initial_state, goal_state, allowed_moves, num_wildcards, max_depth=30, timeout=100):** Performs A\* search with wildcard heuristic, depth, and timeout limits.
- **format_solution_for_submission(puzzle_id, solution_moves):** Formats the solution moves for submission.
- **solve_puzzles(puzzles_df, puzzle_info_df, sample_submission_df, num_puzzles=None, limit_index=30):** Solves puzzles using A\* search and wildcard heuristics, generating a submission DataFrame.

The main script loads data, parses puzzle status, solves the puzzles, and saves the submission file.

## References

- [Santa 2023 Kaggle Competition](https://www.kaggle.com/competitions/santa-2023/overview)
- [Kaggle Data Page](https://www.kaggle.com/competitions/santa-2023/data)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
