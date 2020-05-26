DATA_FILE = 'spy.txt'
DATA_SEP = '|'
SOURCE_FILE = '333.txt'


def get_pieces(lines):
    pieces = []
    piece = ""
    for line in lines[1::]:
        # split
        if line.startswith(DATA_SEP):
            ws = line[1::].split(DATA_SEP)
            ws[0] = DATA_SEP
        else:
            ws = line.split(DATA_SEP)
        ch = ws[0]

        # analysis
        if ch in '1234567890-=\\qwertyuiop[]asdfghjkl;''zxcvbnm,./~!@#$%^&*()_+|QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?':
            piece += ch
        elif ch == 'space':
            piece += ' '
        elif ch == 'enter':
            piece += '\n'
        elif ch == 'backspace':
            piece = piece[0:-1:]
        else:
            # append
            if piece != "":
                pieces.append(piece)
                piece = ""
    pieces.reverse()
    return pieces


# -------- main ---------
with open(DATA_FILE, 'r') as f:
    lines = f.readlines()
pieces = get_pieces(lines)

# covering
with open(SOURCE_FILE, 'r') as f:
    source = f.read()

sub = 'a'
for piece in pieces:
    ri = source.rfind(piece)
    if ri != -1:
        rj = ri + len(piece)
        xxx = sub * len(piece)
        sub = chr(ord(sub) + 1)
        source = source[:ri:] + xxx + source[rj::]


print(source)



print(pieces)

