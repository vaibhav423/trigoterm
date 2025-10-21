import math
import os
import sys
import time
from colors import Colors
import select
import termios
import tty

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

def get_user_input():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("\n" + Colors.LIGHT_WHITE + "Select trigonometric functions to display:" + Colors.END)
    print(Colors.GREEN + "1. sin(x)" + Colors.END)
    print(Colors.CYAN + "2. cos(x)" + Colors.END)
    print(Colors.PURPLE + "3. sec(x)" + Colors.END)
    print(Colors.LIGHT_RED + "4. cosec(x)" + Colors.END)
    print(Colors.BROWN + "5. tan(x)" + Colors.END)
    print(Colors.LIGHT_BLUE + "6. cot(x)" + Colors.END)
    print("\nEnter numbers separated by spaces (e.g., '1 3' for sin and sec): ", end="")
    
    
    user_input = input().strip()
    
    
    selected_functions = []
    try:
        numbers = user_input.split()
        for num in numbers:
            func_num = int(num)
            if 1 <= func_num <= 6:
                selected_functions.append(func_num)
    except ValueError:
        pass
    
    return list(set(selected_functions))  

def main():
    
    selected_functions = get_user_input()
    
    if not selected_functions:
        print(Colors.RED + "No valid functions selected. Returning to main menu." + Colors.END)
        time.sleep(2)
        return
    
    print(f"\nDisplaying functions: {selected_functions}")
    print("Press Ctrl+C to return to main menu...")
    time.sleep(2)
    
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
        cosec_history = []
        cot_history = []

    
        functions = {
            1: {'name': 'sin', 'history': sin_history, 'color': Colors.GREEN, 'char': 's', 'scale': 1},
            2: {'name': 'cos', 'history': cos_history, 'color': Colors.CYAN, 'char': 'c', 'scale': 1},
            3: {'name': 'sec', 'history': sec_history, 'color': Colors.PURPLE, 'char': 'S', 'scale': 2},
            4: {'name': 'cosec', 'history': cosec_history, 'color': Colors.LIGHT_RED, 'char': 'C', 'scale': 2},
            5: {'name': 'tan', 'history': tan_history, 'color': Colors.BROWN, 'char': 't', 'scale': 4},
            6: {'name': 'cot', 'history': cot_history, 'color': Colors.LIGHT_BLUE, 'char': 'T', 'scale': 4}
        }

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
            
    
            values = {}
            values[1] = sin_val  # sin
            values[2] = cos_val  # cos
            
    
            if abs(cos_val) > 1e-9:
                values[3] = 1 / cos_val  # sec
            else:
                values[3] = float('inf')
                
            if abs(sin_val) > 1e-9:
                values[4] = 1 / sin_val  # cosec
            else:
                values[4] = float('inf')
            
            # tan and cot
            if abs(cos_val) > 1e-9:
                values[5] = sin_val / cos_val  # tan
            else:
                values[5] = float('inf') if sin_val > 0 else float('-inf')
                
            if abs(sin_val) > 1e-9:
                values[6] = cos_val / sin_val  # cot
            else:
                values[6] = float('inf') if cos_val > 0 else float('-inf')

            
            for func_num in selected_functions:
                functions[func_num]['history'].insert(0, values[func_num])

            
            wave_len = width - (center_x + int(radius * 2) + 4)
            for func_num in selected_functions:
                hist = functions[func_num]['history']
                if len(hist) > wave_len:
                    hist.pop()

            
            for func_num in selected_functions:
                func_info = functions[func_num]
                history = func_info['history']
                color = func_info['color']
                char = func_info['char']
                scale = func_info['scale']
                
                for i, val in enumerate(history):
                    if abs(val) != float('inf'):
                        x = center_x + int(radius * 2) + 4 + i
                        y = int(center_y - val * radius / scale)
                        if 0 <= x < width and 0 <= y < height:
                            screen[y][x] = color + char + Colors.END

            
            arrow_head_x = center_x + radius * 2 * cos_val
            arrow_head_y = center_y - radius * sin_val
            draw_line(screen, center_x, center_y, arrow_head_x, arrow_head_y, '*', Colors.RED, width, height)

            
            for row in screen:
                print("".join(row))

            
            print(f"Angle: {angle}°")
            for func_num in selected_functions:
                func_info = functions[func_num]
                val = values[func_num]
                if abs(val) == float('inf'):
                    val_str = "∞" if val > 0 else "-∞"
                else:
                    val_str = f"{val:.2f}"
                print(func_info['color'] + f"{func_info['name']}({angle}°) = {val_str}" + Colors.END)


            print("\n" + Colors.LIGHT_WHITE + "info:" + Colors.END)
            for func_num in selected_functions:
                func_info = functions[func_num]
                print(func_info['color'] + f"{func_num}. {func_info['name']}(x) - '{func_info['char']}'" + Colors.END, end="  ")
            print()

            angle = (angle + 5) % 360
            time.sleep(0.15)
            
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
