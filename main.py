import math
import os
import sys
import time
from colors import Colors
import select
import subprocess

def main():
    angle = 0
    selected_option = 0
    menu_options = [
        "1. Sine and Cosine",
        "2. Secant and Tangent",
        "3. Cosecant and Cotangent",
        "4. Exit"
    ]
    
    title_art = [
        "░▒▓████████▓▒░▒▓███████▓▒░░▒▓█▓▒░░▒▓██████▓▒░ ░▒▓██████▓▒░▒▓████████▓▒░▒▓████████▓▒░▒▓███████▓▒░░▒▓██████████████▓▒░  ",
        "   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░ ",
        "   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░ ",
        "   ░▒▓█▓▒░   ░▒▓███████▓▒░░▒▓█▓▒░▒▓█▓▒▒▓███▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓██████▓▒░ ░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░ ",
        "   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░ ",
        "   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░ ",
        "   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓██████▓▒░ ░▒▓██████▓▒░  ░▒▓█▓▒░   ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░"
    ]

    def get_char_non_blocking():
        if os.name == 'nt':
            import msvcrt
            if msvcrt.kbhit():
                return msvcrt.getch()
        else:
            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                c = sys.stdin.read(1)
                if ord(c) == 27:  # ESC character (0x1b)
                    # Read the next characters for arrow keys
                    if select.select([sys.stdin], [], [], 0.01) == ([sys.stdin], [], []):
                        c2 = sys.stdin.read(1)
                        if c2 == '[':
                            if select.select([sys.stdin], [], [], 0.01) == ([sys.stdin], [], []):
                                c3 = sys.stdin.read(1)
                                if c3 == 'A':
                                    return 'up'
                                elif c3 == 'B':
                                    return 'down'
                                elif c3 == 'C':
                                    return 'right'
                                elif c3 == 'D':
                                    return 'left'
                return c
        return None

    try:
        while True:
            try:
                width, height = os.get_terminal_size()
            except OSError:
                width, height = 80, 24

            radius = min(width // 6, height // 3) - 2

            center_x = width // 2
            center_y = height // 2

            os.system('cls' if os.name == 'nt' else 'clear')

            screen = [[' ' for _ in range(width)] for _ in range(height)]
            
            title_width = len(title_art[0])
            title_x = (width - title_width) // 2
            title_y = 1
            for i, line in enumerate(title_art):
                for j, char in enumerate(line):
                    if 0 <= title_y + i < height and 0 <= title_x + j < width:
                        screen[title_y + i][title_x + j] = Colors.LIGHT_WHITE + char + Colors.END

            for i in range(361):
                rad = math.radians(i)
                x = int(center_x + radius * 2 * math.cos(rad))
                y = int(center_y + radius * math.sin(rad))
                if 0 <= x < width and 0 <= y < height:
                    screen[y][x] = Colors.YELLOW + '●' + Colors.END

            for i in range(width):
                if 0 <= center_y < height:
                    screen[center_y][i] = Colors.LIGHT_WHITE + '─' + Colors.END
            for i in range(height):
                if 0 <= center_x < width:
                    screen[i][center_x] = Colors.LIGHT_WHITE + '│' + Colors.END
            if 0 <= center_x < width and 0 <= center_y < height:
                screen[center_y][center_x] = Colors.LIGHT_WHITE + '┼' + Colors.END

            arrow_head_x = int(center_x + radius * 2 * math.cos(math.radians(angle)))
            arrow_head_y = int(center_y + radius * math.sin(math.radians(angle)))

            x1, y1 = center_x, center_y
            x2, y2 = arrow_head_x, arrow_head_y
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            sx = 1 if x1 < x2 else -1
            sy = 1 if y1 < y2 else -1
            err = dx - dy

            while True:
                if 0 <= y1 < height and 0 <= x1 < width:
                    screen[y1][x1] = Colors.RED + '•' + Colors.END
                if x1 == x2 and y1 == y2:
                    break
                e2 = 2 * err
                if e2 > -dy:
                    err -= dy
                    x1 += sx
                if e2 < dx:
                    err += dx
                    y1 += sy
            
            if 0 <= arrow_head_y < height and 0 <= arrow_head_x < width:
                screen[arrow_head_y][arrow_head_x] = Colors.RED + '@' + Colors.END

            for row in screen:
                print("".join(row))

            print(f"\033[{height - len(menu_options) - 2};0H", end="")
            print("Press a number to select a trigonometric function pair:")
            for option in menu_options:
                print(f"  {option}")

            choice = get_char_non_blocking()

            if choice:
                if choice == '1':
                    script_to_run = "trigo_circle.py"
                    if os.name != 'nt':
                        import termios
                        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                    
                    try:
                        subprocess.run([sys.executable, script_to_run])
                    except KeyboardInterrupt:
                        pass

                    if os.name != 'nt':
                        import tty
                        tty.setcbreak(sys.stdin.fileno())
                        
                elif choice == '2':
                    script_to_run = "trigo_circle_sec_tan.py"
                    if os.name != 'nt':
                        import termios
                        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                    
                    try:
                        subprocess.run([sys.executable, script_to_run])
                    except KeyboardInterrupt:
                        pass

                    if os.name != 'nt':
                        import tty
                        tty.setcbreak(sys.stdin.fileno())
                        
                elif choice == '3':
                    script_to_run = "trigo_circle_cot_cosec.py"
                    if os.name != 'nt':
                        import termios
                        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                    
                    try:
                        subprocess.run([sys.executable, script_to_run])
                    except KeyboardInterrupt:
                        pass

                    if os.name != 'nt':
                        import tty
                        tty.setcbreak(sys.stdin.fileno())
                        
                elif choice == '4':
                    break

            angle = (angle + 5) % 360

            time.sleep(0.1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    if os.name != 'nt':
        import tty
        import termios
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setcbreak(sys.stdin.fileno())
            main()
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    else:
        main()
