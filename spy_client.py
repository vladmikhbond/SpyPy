import keyboard
import datetime
import win32gui

DATA_SEP = '|'
SESSION_START = datetime.datetime.now()
QUIT_KEY = 'ctrl+shift+q'
last_win_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())

log = []


def main_hook(e):
    global last_win_title, log
    # def windows title
    curr_win_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    if curr_win_title == last_win_title:
        curr_win_title = '-'
    else:
        last_win_title = curr_win_title
    # def time in msec
    diff_in_msec = int((datetime.datetime.now() - SESSION_START).total_seconds() * 1000)

    log.append([e.name, diff_in_msec, curr_win_title])


def save_to_file():
    global log
    path = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.txt'
    
    with open(path, 'w', encoding="utf-8") as f:
        print(SESSION_START, file=f)
        for x in log:
            print(x[0], x[1], x[2], sep=DATA_SEP, file=f)


def clear_log():
    """
    clear from ctr+ctr+ctr+ctr+c+c+c+c+c
    clear from ctr+ctr+ctr+ctr+v+v+v+v+v
    """
    global log
    state = "normal"
    i = i0 = 0
    while i < len(log):
        x = log[i][0]
        if state == "normal":
            if x == 'ctrl':
                state = "ctrl"
                i0 = i
        elif state == "ctrl":
            if x == 'ctrl':
                pass
            elif x == 'c':
                state = "ctrl+c"
            elif x == 'v':
                state = "ctrl+v"
            else:
                state = "normal"
        elif state == "ctrl+c" and x != 'c' or state == "ctrl+v" and x != 'v':
            state = "normal"
            log = log[:i0:] + log[i::]
            i = i0
        i += 1


# ------------------ main -------------------
# wait
keyboard.on_press(main_hook)
keyboard.add_hotkey(QUIT_KEY, lambda: None)
keyboard.wait(QUIT_KEY)
# stop
keyboard.unhook_all()
clear_log()
save_to_file()
