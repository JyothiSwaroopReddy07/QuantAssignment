
import sys, pathlib


FULL_ROW = (1 << 10) - 1                

SHAPES = {                             
    'Q': [0b11, 0b11],        
    'I': [0b1111],                  
    'T': [0b111, 0b010],          
    'L': [0b111, 0b100],      
    'J': [0b111, 0b001],        
    'Z': [0b110, 0b011],        
    'S': [0b011, 0b110]         
}


def drop_piece(board, template, col):

    shape = [row << col for row in template]        

    row = len(board) + 4                        
    while True:
        nxt = row - 1
        blocked = False
        for dy, bits in enumerate(shape):
            y = nxt + dy
            if y < 0 or (y < len(board) and board[y] & bits):
                blocked = True
                break
        if blocked:
            break
        row = nxt                                

    for dy, bits in enumerate(shape):
        y = row + dy
        if y >= len(board):
            board.extend([0] * (y + 1 - len(board)))
        board[y] |= bits

def clear_rows(board):
    """Strip full rows and compact the board."""
    compact = [r for r in board if r != FULL_ROW]
    while compact and compact[-1] == 0:             
        compact.pop()
    return compact

def board_height(board):
    for y in range(len(board) - 1, -1, -1):
        if board[y]:
            return y + 1
    return 0


def solve(in_path: str, out_path: str):
    with open(in_path, 'r', encoding='utf-8') as fin, \
         open(out_path, 'w', encoding='utf-8') as fout:

        for line in fin:
            line = line.strip()
            if not line:
                fout.write('0\n')                  
                continue

            board = []                             
            for token in line.split(','):
                piece, col = token[0], int(token[1:])
                drop_piece(board, SHAPES[piece], col)
                board = clear_rows(board)

            fout.write(str(board_height(board)) + '\n')


if __name__ == '__main__':
    default_in  = 'Challenge_Input.txt'
    default_out = 'Output.txt'

    in_file  = sys.argv[1] if len(sys.argv) > 1 else default_in
    out_file = sys.argv[2] if len(sys.argv) > 2 else default_out

    if not pathlib.Path(in_file).is_file():
        sys.exit(f"Input file '{in_file}' not found.")

    solve(in_file, out_file)
    print(f"Done. Heights written to '{out_file}'.")
