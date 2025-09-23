from time import sleep
import sys

print("Generating, please wait     ", end='', flush=True)

while True:
    for symbol in [".   ", "..  ", "... ", "...."]:
        sys.stdout.write('\b\b\b\b\b' + symbol)  # Move the cursor back to overwrite the previous ellipsis
        sys.stdout.flush()
        sleep(0.5)
