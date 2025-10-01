import math
import os
import time
from colors import Colors

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

        while True:
            os.system('cls' if os.name == 'nt' else 'clear')

            screen = [[' ' for _ in range(width)] for _ in range(height)]

            for i in range(361):
                rad = math.radians(i)
                x = int(center_x + radius * 2 * math.cos(rad))
                y = int(center_y + radius * math.sin(rad))
                if 0 <= x < width and 0 <= y < height:
                    screen[y][x] = Colors.YELLOW + '.' + Colors.END

            for i in range(width):
                if 0 <= center_y < height:
                    screen[center_y][i] = Colors.LIGHT_WHITE + '-' + Colors.END
            for i in range(height):
                if 0 <= center_x < width:
                    screen[i][center_x] = Colors.LIGHT_WHITE + '|' + Colors.END

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
                    screen[y1][x1] = Colors.RED + '*' + Colors.END
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

            cos_val = math.cos(math.radians(angle))
            sin_val = math.sin(math.radians(angle))

            sin_history.insert(0, sin_val)
            cos_history.insert(0, cos_val)
            if len(sin_history) > width - (center_x + radius * 2 + 2):
                sin_history.pop()
            if len(cos_history) > height - (center_y + radius + 2):
                cos_history.pop()

            for i, val in enumerate(sin_history):
                x = center_x + radius * 2 + 2 + i
                y = int(center_y + val * radius)
                if 0 <= x < width and 0 <= y < height:
                    screen[y][x] = Colors.GREEN + 's' + Colors.END

            for i, val in enumerate(cos_history):
                x = int(center_x + val * radius * 2)
                y = center_y + radius + 2 + i
                if 0 <= x < width and 0 <= y < height:
                    screen[y][x] = Colors.CYAN + 'c' + Colors.END

            for i in range(center_x + int(radius*2), arrow_head_x, -1):
                if 0 <= arrow_head_y < height and 0 <= i < width:
                    screen[arrow_head_y][i] = Colors.LIGHT_BLUE + '.' + Colors.END
            for i in range(center_y + radius, arrow_head_y, -1):
                if 0 <= i < height and 0 <= arrow_head_x < width:
                    screen[i][arrow_head_x] = Colors.LIGHT_BLUE + '.' + Colors.END

            for row in screen:
                print("".join(row))

            print(f"Angle: {angle}°")
            print(Colors.CYAN + f"cos({angle}°) = {cos_val:.2f}" + Colors.END)
            print(Colors.GREEN + f"sin({angle}°) = {sin_val:.2f}" + Colors.END)

            angle = (angle + 5) % 360

            time.sleep(0.1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
