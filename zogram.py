import sys
from z3 import Solver, Bool, And, Or, Not, sat, is_true
import numpy as np
from PIL import Image
from typing import List

def _add_line_constraints(
    solver: Solver,
    all_clues: List[List[int]],
    grid: List[List],
    orientation: str
) -> None:
    if orientation == 'row':
        num_lines = len(grid)
        line_length = len(grid[0]) if num_lines > 0 else 0
    elif orientation == 'col':
        num_lines = len(grid[0]) if grid else 0
        line_length = len(grid)
    else:
        raise ValueError("Orientation must be 'row' or 'col'")

    for i in range(num_lines):
        clues = all_clues[i]
        
        if orientation == 'row':
            line_vars = grid[i]
        else:
            line_vars = [grid[row_idx][i] for row_idx in range(line_length)]

        if not clues:
            solver.add(And([Not(var) for var in line_vars]))
            continue

        possible_placements = []

        def _generate_placements(block_idx: int, start_pos: int, placements: List[int]):
            if block_idx == len(clues):
                is_filled = [False] * line_length
                for k, start in enumerate(placements):
                    for offset in range(clues[k]):
                        is_filled[start + offset] = True
                
                pattern = And([
                    var if is_filled[j] else Not(var)
                    for j, var in enumerate(line_vars)
                ])
                possible_placements.append(pattern)
                return

            current_block_size = clues[block_idx]
            remaining_blocks_size = sum(clues[block_idx:])
            separators_needed = len(clues) - block_idx - 1
            max_start = line_length - remaining_blocks_size - separators_needed
            
            for start in range(start_pos, max_start + 1):
                next_start_pos = start + current_block_size + 1
                _generate_placements(block_idx + 1, next_start_pos, placements + [start])

        _generate_placements(block_idx=0, start_pos=0, placements=[])

        if possible_placements:
            solver.add(Or(possible_placements))
        else:
            solver.add(Bool(False))

def solve_nonogram(
    row_clues: List[List[int]],
    column_clues: List[List[int]],
    filename: str = "nonogram_solution.png",
    scale: int = 20,
    check_uniqueness: bool = True
) -> None:
    STATUS_WORKING = "[*]"
    STATUS_SUCCESS = "[/]"
    STATUS_FAIL    = "[X]"
    STATUS_INFO    = "[!]"

    N = len(row_clues)
    M = len(column_clues)
    
    if N == 0 or M == 0:
        print(f"{STATUS_FAIL} Error: Row or column clues cannot be empty.")
        return

    grid = [[Bool(f"pixel_{r}_{c}") for c in range(M)] for r in range(N)]
    solver = Solver()

    _add_line_constraints(solver, row_clues, grid, 'row')
    _add_line_constraints(solver, column_clues, grid, 'col')

    print(f"{STATUS_WORKING} Solving puzzle...", end='', flush=True)
    
    padding = " " * 20 

    if solver.check() == sat:
        print(f"\r{STATUS_SUCCESS} Solution found!{padding}")
        model = solver.model()

        solution_matrix = np.array([
            [0 if is_true(model[grid[r][c]]) else 255 for c in range(M)]
            for r in range(N)
        ], dtype=np.uint8)

        img = Image.fromarray(solution_matrix, 'L')
        img = img.resize((M * scale, N * scale), Image.NEAREST)
        img.save(filename)
        print(f"{STATUS_SUCCESS} Image saved as {filename}")
        
        if check_uniqueness:
            print(f"{STATUS_WORKING} Checking for uniqueness...", end='', flush=True)
            
            blocking_clause = Or([
                var != model[var] for row in grid for var in row
            ])
            solver.add(blocking_clause)

            if solver.check() == sat:
                print(f"\r{STATUS_INFO} The solution is NOT unique.{padding}")
            else:
                print(f"\r{STATUS_SUCCESS} The solution is UNIQUE.{padding}")
        
        img.show()

    else:
        print(f"\r{STATUS_FAIL} No solution exists for the given clues.{padding}")

if __name__ == '__main__':
    rows = [
        [], [4], [6], [2, 2], [2, 2],
        [6], [4], [2], [2], [2], []
    ]

    cols = [
        [], [9], [9], [2, 2], [2, 2],
        [4], [4], []
    ]

    solve_nonogram(rows, cols, "checkmark.png", scale=30, check_uniqueness=True)
