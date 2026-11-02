#!/usr/bin/env python3

import os
import random
import sys
import time
import termios
import tty
import select

def get_key():
    if select.select([sys.stdin], [], [], 0)[0]:
        return sys.stdin.read(1)
    return None

def rain():
    old_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setcbreak(sys.stdin.fileno())

        try:
            columns, rows = os.get_terminal_size()
        except OSError:
            columns, rows = 80, 24;

        # Hide terminal cursor
        sys.stdout.write("\033[2J\033[?25l")
        sys.stdout.flush()

        # Track Y pos per columns
        drops = [random.randint(-rows, 0) for _ in range(columns)]

        # The character pool
        chars = "39MIKU"

        # Default speed
        speed = 0.05
        try:
            while True:
                # Speed keybinds
                key = get_key()
                if key == '+':
                    speed = max(0.002, speed - 0.005)
                elif key == '-':
                    speed = min(0.3, speed + 0.005)

                # Re-checking terminal size
                try:
                    current_cols, current_rows = os.get_terminal_size()
                    if current_cols != columns or current_rows != rows:
                        columns, rows = current_cols, current_rows
                        drops = [random.randint(-rows, 0) for _ in range(columns)]
                        sys.stdout.write("\033[2J")
                except OSError:
                    pass

                for col in range(columns):
                    y = drops[col]
                    trail_length = 15
                    y_to_delete = y - trail_length

                    if y_to_delete >= 0 and y_to_delete < rows:
                        sys.stdout.write(f"\033[{y_to_delete + 1};{col + 1}H\033[40m ")

                    # Only draw if drop is within the visible screen
                    if y >= 0 and y < rows:
                        char = random.choice(chars)
                        sys.stdout.write(f"\033[{y + 1};{col + 1}H")

                        # Colors
                        if random.random() > 0.98:
                            sys.stdout.write(f"\033[1;37m{char}")
                        else:
                            sys.stdout.write(f"\033[1;36m{char}")

                    drops[col] += 1

                    # If stream hits the bottom or resets, send it back at the top
                    if drops[col] >= rows + trail_length:
                        drops[col] = random.randint(-5, 0)

                sys.stdout.flush()
                time.sleep(speed) # Speed of the rain

        except KeyboardInterrupt:
            pass

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        sys.stdout.write("\033[?25h\033[0m\033[2J\033[1;1H")
        sys.stdout.flush()
        print("\nMiku matrix closed. See you later~ >:3")


if __name__ == "__main__":
    rain()
