```
FILE: README.MD
DESC: Instructions for zogram.py

# ===================
# 1. PREREQUISITES
# ===================
# - Python 3.x

# ===================
# 2. SETUP
# ===================

$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install z3-solver numpy Pillow

# ===================
# 3. EXECUTION
# ===================

(venv) $ python zogram.py

# --- EXPECTED OUTPUT (TERMINAL) ---
# [/] Solution found!
# [/] Image saved as checkmark.png
# [/] The solution is UNIQUE.
# ------------------------------------

# A file `checkmark.png` is created.
# An image window opens.


# ===================
# 4. CUSTOM PUZZLE
# ===================

# 1. Edit `if __name__ == '__main__':` block in `zogram.py`.

# --- BEFORE ---
#     rows = [
#         [], [4], [6], [2, 2], [2, 2],
#         [6], [4], [2], [2], [2], []
#     ]
#     cols = [
#         [], [9], [9], [2, 2], [2, 2],
#         [4], [4], []
#     ]
#     solve_nonogram(rows, cols, "checkmark.png", scale=30)
# ----------------

# --- AFTER (EXAMPLE) ---
#     rows = [[1, 1], [3], [1, 1]]
#     cols = [[1, 1], [3], [1, 1]]
#     solve_nonogram(rows, cols, "x_puzzle.png", scale=40)
# -----------------------

# 2. Save the file and re-run the execution command.
```
