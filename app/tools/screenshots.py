import time
import pyautogui


def take_screenshot():
    filename = f"screenshot_{int(time.time())}.png"

    pyautogui.screenshot(filename)

    return f"I took a screenshot and saved it as {filename}."


def handle_screenshot_command(text):
    text = text.lower().strip()

    if "take a screenshot" in text or "take screenshot" in text:
        return take_screenshot()

    return None