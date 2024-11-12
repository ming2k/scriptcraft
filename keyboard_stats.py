#!/usr/bin/env python3

import csv
import evdev
from evdev import InputDevice, categorize, ecodes
from collections import Counter
import threading
import time
import os
import select
import argparse

SAVE_INTERVAL = 60  # 保存间隔（秒）

key_counter = Counter()

def load_existing_data(csv_file):
    if os.path.exists(csv_file):
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 2:
                    key_counter[row[0]] = int(row[1])

def save_data(csv_file):
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        for key, count in key_counter.items():
            writer.writerow([key, count])

def periodic_save(csv_file):
    while True:
        time.sleep(SAVE_INTERVAL)
        save_data(csv_file)
        print(f"Data saved at {time.ctime()}")

def is_keyboard(device):
    keyboard_names = ['keyboard', 'keybrd', 'keypad']
    if not any(name in device.name.lower() for name in keyboard_names):
        return False

    required_keys = {
        evdev.ecodes.KEY_Q, evdev.ecodes.KEY_W, evdev.ecodes.KEY_E, evdev.ecodes.KEY_R,
        evdev.ecodes.KEY_A, evdev.ecodes.KEY_S, evdev.ecodes.KEY_D, evdev.ecodes.KEY_F,
        evdev.ecodes.KEY_Z, evdev.ecodes.KEY_X, evdev.ecodes.KEY_C, evdev.ecodes.KEY_V,
        evdev.ecodes.KEY_1, evdev.ecodes.KEY_2, evdev.ecodes.KEY_3,
        evdev.ecodes.KEY_SPACE, evdev.ecodes.KEY_ENTER, evdev.ecodes.KEY_BACKSPACE,
        evdev.ecodes.KEY_LEFTSHIFT, evdev.ecodes.KEY_RIGHTSHIFT,
        evdev.ecodes.KEY_LEFTCTRL, evdev.ecodes.KEY_RIGHTCTRL
    }
    
    capabilities = device.capabilities().get(evdev.ecodes.EV_KEY, [])
    return all(key in capabilities for key in required_keys)

def find_keyboards():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    keyboards = [device for device in devices if is_keyboard(device)]
    return keyboards

def update_key_counter(keycode):
    if isinstance(keycode, list):
        for code in keycode:
            key_counter[str(code)] += 1
    else:
        key_counter[str(keycode)] += 1

def main(csv_file):
    load_existing_data(csv_file)

    save_thread = threading.Thread(target=periodic_save, args=(csv_file,))
    save_thread.daemon = True
    save_thread.start()

    keyboards = find_keyboards()
    if not keyboards:
        print("No keyboards found")
        return

    print("Monitoring keyboards:")
    for keyboard in keyboards:
        print(f"- {keyboard.name}")

    devices = {dev.fd: dev for dev in keyboards}

    while True:
        r, w, x = select.select(devices, [], [])
        for fd in r:
            for event in devices[fd].read():
                if event.type == ecodes.EV_KEY:
                    key_event = categorize(event)
                    if key_event.keystate == key_event.key_down:
                        update_key_counter(key_event.keycode)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Keyboard Statistics Collector")
    parser.add_argument("csv_file", help="Path to the CSV file for storing key press data")
    args = parser.parse_args()

    try:
        main(args.csv_file)
    except KeyboardInterrupt:
        print("Keyboard Interrupt detected. Saving data...")
        save_data(args.csv_file)
        print("Data saved. Exiting...")
    except PermissionError:
        print("Permission denied. Try running the script with sudo.")
