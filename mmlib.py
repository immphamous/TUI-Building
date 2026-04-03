import sys, termios, tty

def set_default(d, default):
    for default_name in default:
        print(default_name)
        print(default)
        default_value = default[default_name]
        d.setdefault(default_name, default_value)
        if isinstance(default_value, dict):
            set_default(d[default_name], default_value)

def clamp(v, mn, mx):
    return max(min(v, mx), mn)

def read_key():
    fd = sys.stdin.fileno()
    orig = termios.tcgetattr(fd)

    try:
        tty.setcbreak(fd)  # or tty.setraw(fd) if you prefer raw mode's behavior.
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, orig)
