"""
Automatically run around in circles to increase the friendship of Pokemon.
Usage for PC Pokemon emulators:
Run "python3 increaseFriendship.py".
Enter the key binded in-game to 'run'.
Enter the desired length of time to hold a direction (in seconds - usually keep this value under one second).
Then click on the Pokemon app.
Press 'esc' to stop the program.
"""

import pyautogui
import sys
import pynput
import threading
import time

DEBUG = False

def on_press(key):
    global esc_pressed
    if DEBUG:
        print(f"{key} pressed")
    if key == pynput.keyboard.Key.esc:
        print("Stopping...")
        with app_lock:
            esc_pressed = True
        move_thread.join()
        mouse_listener.stop()
        keyboard_listener.stop()

def on_click(x, y, button, pressed):
    global isTraining
    if pressed:
        if DEBUG:
            print(f"{button} clicked at ({x}, {y})")
        print("Friendship farming in progress!")
        print("Press esc to stop...")
        with app_lock:
            isTraining = True
            time.sleep(0.5)

def move():
    global isTraining
    global length
    global run_key
    while True:
        with app_lock:
            if esc_pressed == True:
                pyautogui.keyUp(run_key)
                pyautogui.keyUp('left')
                pyautogui.keyUp('right')
                pyautogui.keyUp('up')
                pyautogui.keyUp('down')
                break
            if isTraining == False:
                continue

            pyautogui.keyDown(run_key)
            time.sleep(0.01)
            pyautogui.keyDown('right')
            time.sleep(length)
            pyautogui.keyUp('right')
            pyautogui.keyDown('down')
            time.sleep(length)
            pyautogui.keyUp('down')
            pyautogui.keyDown('left')
            time.sleep(length)
            pyautogui.keyUp('left')
            pyautogui.keyDown('up')
            time.sleep(length)
            pyautogui.keyUp('up')
            pyautogui.keyUp(run_key)
            time.sleep(0.01)

# Threads
mouse_listener =  pynput.mouse.Listener(on_click=on_click)
keyboard_listener = pynput.keyboard.Listener(on_press=on_press)
move_thread = threading.Thread(target=move, args=())
move_thread.daemon = True

# Global vars
length = 0
run_key = 'z'
isTraining = False
esc_pressed = False
app_lock = threading.Lock() # Protects global flag "isTraining"

def main():
    global length
    global run_key
    print("Please enter the held key you have binded in-game to 'run' (a-z):")
    run_key = sys.stdin.readline().strip()
    print("Please enter the number of seconds to hold a direction:")
    length = float(sys.stdin.readline().strip())
    print("Click on your Pokemon app to begin increasing Friendship...")

    mouse_listener.start()
    move_thread.start()
    keyboard_listener.start()
    
    keyboard_listener.join()
    mouse_listener.join()
    print("Done")
    sys.exit()

if __name__ == "__main__":
    main()
