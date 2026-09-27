import os
import subprocess
from pathlib import Path


WINDOWS_APPS = {
    "notepad": "notepad.exe",
    "calculator": "CalculatorApp.exe",
    "paint": "mspaint.exe",
    "file explorer": "explorer.exe",
    "explorer": "explorer.exe",
    "command prompt": "cmd.exe",
    "cmd": "cmd.exe",
    "powershell": "powershell.exe",
    "task manager": "Taskmgr.exe",
    "control panel": "control.exe",
    "snipping tool": "SnippingTool.exe",
}


def find_installed_app(app_name):
    """
    Search Windows Start Menu for an installed application.
    """

    app_name = app_name.lower().strip()

    search_locations = [
        Path(os.environ.get("PROGRAMDATA", "C:\\ProgramData"))
        / "Microsoft"
        / "Windows"
        / "Start Menu"
        / "Programs",

        Path(os.environ.get("APPDATA", ""))
        / "Microsoft"
        / "Windows"
        / "Start Menu"
        / "Programs",
    ]

    for location in search_locations:

        if not location.exists():
            continue

        try:

            for shortcut in location.rglob("*.lnk"):

                if shortcut.stem.lower() == app_name:
                    return str(shortcut)

        except PermissionError:
            continue

    return None


def open_app(app_name):
    """
    Open a Windows application.
    """

    app_name = app_name.lower().strip()

    executable = WINDOWS_APPS.get(app_name)

    if executable:

        try:
            subprocess.Popen(
                executable,
                shell=True
            )

            return f"Opening {app_name}."

        except Exception:
            return f"I couldn't open {app_name}."

    shortcut = find_installed_app(app_name)

    if shortcut:

        try:
            os.startfile(shortcut)

            return f"Opening {app_name}."

        except Exception:
            return f"I found {app_name}, but couldn't open it."

    return None


def close_app(app_name):
    """
    Close a running Windows application.
    """

    app_name = app_name.lower().strip()

    # Known applications
    executable = WINDOWS_APPS.get(app_name)

    if executable:

        process_name = Path(executable).name

    else:

        # Common application executable names
        process_name = app_name.replace(" ", "") + ".exe"

    try:

        result = subprocess.run(
            [
                "taskkill",
                "/IM",
                process_name,
                "/F"
            ],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return f"Closed {app_name}."

        return None

    except Exception:
        return None


def handle_app_command(text):
    """
    Handle commands such as:

    Open Spotify
    Open Discord
    Close Spotify
    Close Notepad
    """

    text = text.lower().strip()

    # OPEN
    if text.startswith("open "):

        requested_app = text[5:].strip()

        return open_app(requested_app)

    # CLOSE
    if text.startswith("close "):

        requested_app = text[6:].strip()

        result = close_app(requested_app)

        if result:
            return result

        return f"I couldn't close {requested_app}."

    return None