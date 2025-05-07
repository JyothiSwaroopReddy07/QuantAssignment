# Simplified Tetris Engine

A Python 3 implementation of the Quanta **Coding Challenge** — a mini‑Tetris simulator that reads tetromino sequences, applies gravity and row‑clearing rules, and outputs the final stack height for each input line.

---

## Project Structure

| File                  | Purpose                                    |
| --------------------- | ------------------------------------------ |
| `tetris.py`           | Main program / engine (bit‑mask optimized) |
| `challenge_input.txt` | Example input sequences (provided)         |
| `output.txt`          | **Generated** results: one height per line |

> **Note**: The engine does **not** use external libraries; only the Python standard library.

---

## Requirements

* Python ≥ 3.6 (tested with 3.11)
* No additional dependencies

---

## Running the Program

### Quick Start

```bash
# Default: reads challenge_input.txt, writes output.txt
python3 tetris.py
```

You should see:

```
Done. Heights written to 'output.txt'.
```

### Custom Files

```bash
python3 tetris.py my_sequences.txt my_results.txt
```

* **`my_sequences.txt`** – any UTF‑8 text file; each line is a comma‑separated list of pieces such as `I0,I4,Q8`.
* **`my_results.txt`** – will be overwritten with one integer per line.

### Smoke Test (no files)

```bash
echo "Q0" | python3 tetris.py - -
```

Using a single dash (`-`) tells the script to read **STDIN** and write **STDOUT**.

---

## Input Format

* Grid width = 10 columns (0‑9).
* Each tetromino is specified as `<LETTER><COLUMN>`.
* Valid letters & fixed orientations:

  * `Q` (square), `I` (line), `T`, `L`, `J`, `Z`, `S`.
* Example line:
  `Q0,I2,I6,I0,I6,I6,Q2,Q4`

Every line is simulated on a **fresh empty board**.

---

## Output Format

One non‑negative integer per input line — the final height (number of occupied rows) after all pieces settle and all full rows clear.

---

## Performance Notes

* **Bit‑mask rows**: each board row is a 10‑bit integer, enabling O(1) collision checks and row clears.
* Handles thousands of sequences well under one second (height ≤ 100 guaranteed by spec).

---

## Algorithm & Code Logic

### Data Model

* **Rows as bit masks**: The board is a list where each element is a 10‑bit integer. A bit set to `1` means the corresponding column has a block. Keeping rows as integers makes collision checks and row clears a single `&` or `==` operation instead of iterating over individual cells.
* **Piece templates**: Each tetromino is stored as a small list of bit‑mask rows (bottom‑up). At runtime the template is horizontally shifted once with `row << col` and reused while dropping.

### Dropping a Piece (`drop_piece`)

1. **Initial height** – Start the piece a few rows above the current board height ( `len(board) + 4` ).
2. **Collision loop** – Repeatedly try to move the piece down by one row (`nxt = row - 1`).
   *For each template row*:

   * If the candidate `y` is below 0 → collision.
   * Else if that board row exists *and* `(board[y] & bits)` is non‑zero → collision.
3. Stop at the first collision attempt; merge the piece bits into `board[y]` rows with `|=`.

### Clearing Rows (`clear_rows`)

* After merging a piece we build a new list **excluding** any row equal to the constant `FULL_ROW = 0b1111111111`.
* Because rows are compacted this way, dropping remaining rows is automatic — no per‑block shifting required.
* Trailing empty rows (`0`) are trimmed to keep `board` minimal.

### Height Calculation

* Scan the board from the top for the first non‑zero row. Height = index + 1. If board is empty, height = 0.

### Complexity

* **Time** → O(number of pieces × constant) — each piece touches ≤ 6 rows and uses only bit operations.
* **Memory** → ≤ 
  ho × 4 bytes where ρ ≤ 100 (board rows), far below the naïve cell matrix.

---

## Example

Input (`challenge_input.txt`):

```
I0,I4,Q8
T1,Z3,I4
Q0,I2,I6,I0,I6,I6,Q2,Q4
```

Output (`output.txt`):

```
1
4
3
```

---

