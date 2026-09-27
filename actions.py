import webbrowser
import subprocess
import os
import time
import pyautogui


# ============================================================
# NOVA COMPUTER ACTIONS
# ============================================================

def open_website(url, name):
    webbrowser.open(url)
    return f"Opening {name}."


def open_windows_app(app_name):
    """
    Try to open a Windows application using Windows search.
    """

    try:
        # Windows Start/Search can find many installed applications
        subprocess.Popen(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                f'Start-Process "{app_name}"'
            ],
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        return f"Opening {app_name}."

    except Exception:
        return None


def handle_command(text):

    text = text.lower().strip()

    # ========================================================
    # WEBSITES
    # ========================================================

    websites = {

        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "spotify": "https://open.spotify.com",
        "whatsapp": "https://web.whatsapp.com",
        "github": "https://github.com",
        "gmail": "https://mail.google.com",
        "google drive": "https://drive.google.com",
        "google docs": "https://docs.google.com",
        "google calendar": "https://calendar.google.com",
        "netflix": "https://www.netflix.com",
        "instagram": "https://www.instagram.com",
        "facebook": "https://www.facebook.com",
        "reddit": "https://www.reddit.com",
        "linkedin": "https://www.linkedin.com",
        "twitter": "https://x.com",
        "x": "https://x.com",
        "chatgpt": "https://chatgpt.com",
        "claude": "https://claude.ai",
        "gemini": "https://gemini.google.com",
    }

    # "open youtube"
    for name, url in websites.items():

        if f"open {name}" in text:

            return open_website(url, name)

    # ========================================================
    # WINDOWS APPLICATIONS
    # ========================================================

    apps = {

        "notepad": "notepad.exe",

        "calculator": "calc.exe",

        "paint": "mspaint.exe",

        "file explorer": "explorer.exe",

        "explorer": "explorer.exe",

        "command prompt": "cmd.exe",

        "cmd": "cmd.exe",

        "powershell": "powershell.exe",

        "task manager": "taskmgr.exe",

        "control panel": "control.exe",

        "settings": "ms-settings:",

        "snipping tool": "snippingtool.exe",

    }

    for name, executable in apps.items():

        if f"open {name}" in text:

            try:

                subprocess.Popen(
                    executable,
                    shell=True
                )

                return f"Opening {name}."

            except Exception:

                return f"I couldn't open {name}."

    # ========================================================
    # COMMON THIRD-PARTY APPS
    # ========================================================

    third_party_apps = {

        "spotify": "Spotify",

        "discord": "Discord",

        "steam": "Steam",

        "vscode": "Visual Studio Code",

        "visual studio code": "Visual Studio Code",

        "chrome": "Google Chrome",

        "edge": "Microsoft Edge",

        "firefox": "Mozilla Firefox",

        "zoom": "Zoom",

        "telegram": "Telegram",

        "slack": "Slack",

        "notion": "Notion",

        "obs": "OBS Studio",

    }

    for name, app_name in third_party_apps.items():

        if f"open {name}" in text:

            result = open_windows_app(app_name)

            if result:

                return result

            return f"I couldn't open {app_name}."

    # ========================================================
    # SCREENSHOT
    # ========================================================

    if "take a screenshot" in text or "take screenshot" in text:

        filename = f"screenshot_{int(time.time())}.png"

        pyautogui.screenshot(filename)

        return f"I took a screenshot and saved it as {filename}."

    # ========================================================
    # RETURN NOTHING
    # ========================================================

    return None