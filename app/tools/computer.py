import os
import subprocess
import time
import webbrowser

import pyautogui


# ============================================================
# OPEN APPLICATION
# ============================================================

def open_application(app_name):

    app_name = app_name.lower().strip()

    common_apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "explorer": "explorer.exe",
        "file explorer": "explorer.exe",
        "command prompt": "cmd.exe",
        "cmd": "cmd.exe",
        "powershell": "powershell.exe",
    }

    executable = common_apps.get(app_name)

    if not executable:
        return None

    try:

        subprocess.Popen(
            executable,
            shell=True
        )

        time.sleep(1)

        return f"Opened {app_name}."

    except Exception as e:

        return f"Couldn't open {app_name}: {e}"


# ============================================================
# OPEN WEBSITE
# ============================================================

def open_website(url):

    try:

        webbrowser.open(url)

        return f"Opened {url}."

    except Exception as e:

        return f"Couldn't open the website: {e}"


# ============================================================
# TYPE TEXT
# ============================================================

def type_text(text):

    try:

        pyautogui.write(
            text,
            interval=0.02
        )

        return "Typed the requested text."

    except Exception as e:

        return f"Couldn't type the text: {e}"


# ============================================================
# PRESS KEY
# ============================================================

def press_key(key):

    try:

        pyautogui.press(key)

        return f"Pressed {key}."

    except Exception as e:

        return f"Couldn't press {key}: {e}"


# ============================================================
# HOTKEY
# ============================================================

def press_hotkey(*keys):

    try:

        pyautogui.hotkey(
            *keys
        )

        return (
            "Pressed "
            + " + ".join(keys)
            + "."
        )

    except Exception as e:

        return f"Couldn't press the hotkey: {e}"


# ============================================================
# TAKE SCREENSHOT
# ============================================================

def take_screenshot():

    try:

        timestamp = time.strftime(
            "%Y%m%d_%H%M%S"
        )

        filename = (
            f"nova_computer_{timestamp}.png"
        )

        path = os.path.join(
            os.getcwd(),
            filename
        )

        screenshot = pyautogui.screenshot()

        screenshot.save(path)

        return (
            f"Screenshot saved to {path}"
        )

    except Exception as e:

        return (
            f"Couldn't take screenshot: {e}"
        )


# ============================================================
# MOVE MOUSE
# ============================================================

def move_mouse(x, y):

    try:

        pyautogui.moveTo(
            x,
            y,
            duration=0.2
        )

        return (
            f"Moved mouse to {x}, {y}."
        )

    except Exception as e:

        return f"Couldn't move the mouse: {e}"


# ============================================================
# CLICK
# ============================================================

def click_mouse():

    try:

        pyautogui.click()

        return "Clicked."

    except Exception as e:

        return f"Couldn't click: {e}"


# ============================================================
# COMPUTER ACTION ROUTER
# ============================================================

def execute_computer_action(
    action,
    **kwargs
):

    if action == "open_app":

        return open_application(
            kwargs.get("app_name", "")
        )

    if action == "open_website":

        return open_website(
            kwargs.get("url", "")
        )

    if action == "type":

        return type_text(
            kwargs.get("text", "")
        )

    if action == "press_key":

        return press_key(
            kwargs.get("key", "")
        )

    if action == "hotkey":

        return press_hotkey(
            *kwargs.get("keys", [])
        )

    if action == "screenshot":

        return take_screenshot()

    if action == "move_mouse":

        return move_mouse(
            kwargs.get("x", 0),
            kwargs.get("y", 0)
        )

    if action == "click":

        return click_mouse()

    return None