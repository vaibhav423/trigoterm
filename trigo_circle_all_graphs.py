import math
import time
from colors import Colors

def draw_line(screen, x1, y1, x2, y2, char, color, width, height):
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        if 0 <= y1 < height and 0 <= x1 < width:
            screen[y1][x1] = color + char + Colors.END
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

def main():
    try:
        width = 120
        height = 50
        radius = 10
        center_x = width // 4
        center_y = height // 2
        angle = 0
        
        sin_history = []
        cos_history = []
        tan_history = []
        sec_history = []

        while True:
            print("\033[H\033[2J", end="")
            screen = [[' ' for _ in range(width)] for _ in range(height)]

            for i in range(361):
                rad = math.radians(i)
                x = center_x + radius * 2 * math.cos(rad)
                y = center_y + radius * math.sin(rad)
                draw_line(screen, x, y, x, y, '.', Colors.YELLOW, width, height)

            draw_line(screen, 0, center_y, width - 1, center_y, '-', Colors.LIGHT_WHITE, width, height)
            draw_line(screen, center_x, 0, center_x, height - 1, '|', Colors.LIGHT_WHITE, width, height)

            rad_angle = math.radians(angle)
            cos_val = math.cos(rad_angle)
            sin_val = math.sin(rad_angle)
            
            if abs(cos_val) > 1e-9:
                tan_val = sin_val / cos_val
                sec_val = 1 / cos_val
            else:
                tan_val = float('inf') if sin_val > 0 else float('-inf')
                sec_val = float('inf')

            sin_history.insert(0, sin_val)
            cos_history.insert(0, cos_val)
            tan_history.insert(0, tan_val)
            sec_history.insert(0, sec_val)

            wave_len = width - (center_x + int(radius * 2) + 4)
            if len(sin_history) > wave_len: sin_history.pop()
            if len(cos_history) > wave_len: cos_history.pop()
            if len(tan_history) > wave_len: tan_history.pop()
            if len(sec_history) > wave_len: sec_history.pop()

            for i, val in enumerate(sin_history):
                x = center_x + int(radius * 2) + 4 + i
                y = int(center_y - val * radius)
                if 0 <= x < width and 0 <= y < height:
                    screen[y][x] = Colors.GREEN + 's' + Colors.END
            
            for i, val in enumerate(cos_history):
                x = center_x + int(radius * 2) + 4 + i
                y = int(center_y - val * radius)
                if 0 <= x < width and 0 <= y < height:
                    screen[y][x] = Colors.CYAN + 'c' + Colors.END

            tan_scale = 4
            for i, val in enumerate(tan_history):
                if abs(val) != float('inf'):
                    x = center_x + int(radius * 2) + 4 + i
                    y = int(center_y - val * tan_scale)
                    if 0 <= x < width and 0 <= y < height:
                        screen[y][x] = Colors.BROWN + 't' + Colors.END
            
            sec_scale = 2
            for i, val in enumerate(sec_history):
                if abs(val) != float('inf'):
                    x = center_x + int(radius * 2) + 4 + i
                    y = int(center_y - val * sec_scale)
                    if 0 <= x < width and 0 <= y < height:
                        screen[y][x] = Colors.PURPLE + 'S' + Colors.END

            arrow_head_x = center_x + radius * 2 * cos_val
            arrow_head_y = center_y - radius * sin_val
            draw_line(screen, center_x, center_y, arrow_head_x, arrow_head_y, '*', Colors.RED, width, height)

            for row in screen:
                print("".join(row))

            print(f"Angle: {angle}°")
            print(Colors.GREEN + f"sin({angle}°) = {sin_val:.2f}" + Colors.END)
            print(Colors.CYAN + f"cos({angle}°) = {cos_val:.2f}" + Colors.END)
            print(Colors.BROWN + f"tan({angle}°) = {tan_val:.2f}" + Colors.END)
            print(Colors.PURPLE + f"sec({angle}°) = {sec_val:.2f}" + Colors.END)

            angle = (angle + 5) % 360
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
