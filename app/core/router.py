from app.tools.apps import handle_app_command
from app.tools.browser import handle_browser_command
from app.tools.screenshots import handle_screenshot_command


def route_command(text):
    """
    Send a user command to the correct Nova tool.

    Returns:
        str: Tool response if a tool handled the command.
        None: If no tool matched.
    """

    # Windows applications
    result = handle_app_command(text)

    if result:
        return result

    # Websites
    result = handle_browser_command(text)

    if result:
        return result

    # Screenshots
    result = handle_screenshot_command(text)

    if result:
        return result

    # Nothing matched
    return None