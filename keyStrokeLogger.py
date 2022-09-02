
# Log keystrokes + durations to a file
import keyboard
from datetime import datetime
import config

'''
Defines a key - duration pair
Note: "sleep" refers to intervals where no key is held down
'''
class KeyEvent:
    def __init__(self, key: str, start_time: float):
        self.key = key
        self.start_time = start_time
        self.end_time = start_time
    
    def duration(self):
        return self.end_time - self.start_time

'''
Defines a keylogger object
'''
class Keylogger:
    def __init__(self, name : str):
        # Keylogger report prefix
        self.name = name
        # A list of KeyEvent
        self.log = []
        # Logger start and end times
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()
        # Report file
        self.filename = ""
        # State to track whether a key is currently being held
        self.isDown = False

    '''
    on_press callback (for KEYDOWN events)
    Insert the pair {key, start_time}
    '''
    def on_press_handler(self, keyboard_event : keyboard.KeyboardEvent):
        # Append new key presses only
        if len(self.log) > 0 and self.log[-1].key == 'sleep':
            self.log[-1].end_time = datetime.today().timestamp()
        if self.isDown == False:
            self.log.append(KeyEvent(keyboard_event.name, keyboard_event.time))
            self.isDown = True
    
    '''
    on_release callback (for KEYUP events)
    Modify the most recent pair to {key, duration}
    '''
    def on_release_handler(self, keyboard_event: keyboard.KeyboardEvent):
        self.log[-1].end_time = keyboard_event.time
        self.isDown = False
        self.log.append(KeyEvent('sleep', datetime.today().timestamp()))
    
    '''
    Create a new a local file and write the current log
    '''
    def report_to_file(self):
        if self.log:
            self.end_dt = datetime.now()
            start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
            end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
            self.filename = f"{config.LOG_FOLDER}/{self.name}-{start_dt_str}_{end_dt_str}.txt" 
            with open(self.filename, "w") as f:
                for key_event in self.log:
                    f.write(f"{key_event.key}: {key_event.duration()}s\n")

    '''
    Begin logging and wait for esc. Then report log to local file.
    '''
    def start(self):
        self.start_dt = datetime.now()
        print(f"{self.start_dt}: Started keylogger. Press 'esc' to stop and report...")
        # Event loop
        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                if event.name == 'esc':
                    if len(self.log) > 0 and self.log[-1].key == 'sleep':
                        self.log[-1].end_time = datetime.today().timestamp()
                    break
                self.on_press_handler(event)
            elif event.event_type == keyboard.KEY_UP:
                self.on_release_handler(event)
        self.report_to_file()
        print(f"{self.end_dt}: Generated new report - {self.filename}")

if __name__ == "__main__":
    prefix = input("Enter a name for the keylogger: ")
    keylogger = Keylogger(prefix)
    keylogger.start()
