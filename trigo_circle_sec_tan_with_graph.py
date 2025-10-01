import math
import os
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
        
        tan_history = []

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
            
            if cos_val != 0:
                tan_val = math.tan(rad_angle)
                sec_val = 1 / cos_val
            else:
                tan_val = float('inf') if sin_val > 0 else float('-inf')
                sec_val = float('inf') if cos_val > 0 else float('-inf')

            arrow_head_x = center_x + radius * 2 * cos_val
            arrow_head_y = center_y - radius * sin_val

            draw_line(screen, center_x, center_y, arrow_head_x, arrow_head_y, '*', Colors.RED, width, height)
            
            if 0 <= arrow_head_y < height and 0 <= arrow_head_x < width:
                screen[int(arrow_head_y)][int(arrow_head_x)] = Colors.RED + '@' + Colors.END

            tangent_line_x = center_x + radius * 2 * (1 if cos_val >= 0 else -1)

            if abs(cos_val) > 1e-9:
                tangent_intersect_y = center_y - (tangent_line_x - center_x) * tan_val
                draw_line(screen, tangent_line_x, center_y, tangent_line_x, tangent_intersect_y, 't', Colors.GREEN, width, height)
                draw_line(screen, center_x, center_y, tangent_line_x, tangent_intersect_y, 's', Colors.CYAN, width, height)

            if abs(tan_val) < 10:
                tan_history.insert(0, tan_val)
            else:
                clamped_val = 10 if tan_val > 0 else -10
                tan_history.insert(0, clamped_val)
            
            max_graph_width = width - (center_x + radius * 2 + 4)
            if len(tan_history) > max_graph_width:
                tan_history.pop()

            graph_start_x = center_x + radius * 2 + 4
            for i, val in enumerate(tan_history):
                x = graph_start_x + i
                y = int(center_y - val * (radius // 3))
                if 0 <= x < width and 0 <= y < height:
                    screen[y][x] = Colors.GREEN + 'T' + Colors.END

            tan_axis_y = center_y
            for x in range(graph_start_x, min(width, graph_start_x + len(tan_history) + 10)):
                if 0 <= tan_axis_y < height and 0 <= x < width:
                    screen[tan_axis_y][x] = Colors.LIGHT_WHITE + '-' + Colors.END

            tan_axis_x = graph_start_x
            for y in range(max(0, center_y - radius), min(height, center_y + radius)):
                if 0 <= y < height and 0 <= tan_axis_x < width:
                    screen[y][tan_axis_x] = Colors.LIGHT_WHITE + '|' + Colors.END

            if len(tan_history) > 0 and abs(cos_val) > 1e-9:
                current_tan_val = tan_history[0]
                if abs(current_tan_val) > 10:
                    current_tan_val = 10 if current_tan_val > 0 else -10
                
                tan_graph_y = int(center_y - current_tan_val * (radius // 3))
                tan_graph_x = graph_start_x
                tangent_end_y = center_y - (tangent_line_x - center_x) * tan_val
                
                if 0 <= tan_graph_y < height and 0 <= tangent_end_y < height:
                    draw_line(screen, tangent_line_x, tangent_end_y, tan_graph_x, tan_graph_y, '.', Colors.LIGHT_BLUE, width, height)

            for row in screen:
                print("".join(row))

            print(f"Angle: {angle}°")
            print(Colors.GREEN + f"tan({angle}°) = {tan_val:.2f}" + Colors.END)
            print(Colors.CYAN + f"sec({angle}°) = {sec_val:.2f}" + Colors.END)
    

            angle = (angle + 5) % 360
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
