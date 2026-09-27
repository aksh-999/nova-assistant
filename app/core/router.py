from app.tools.apps import handle_app_command
from app.tools.browser import handle_browser_command
from app.tools.screenshots import handle_screenshot_command
from app.core.task_planner import run_task


def route_command(text):

    # Existing app commands
    result = handle_app_command(text)

    if result:
        return result

    # Existing browser commands
    result = handle_browser_command(text)

    if result:
        return result

    # Existing screenshot commands
    result = handle_screenshot_command(text)

    if result:
        return result

    # Simple computer commands
    lower_text = text.lower().strip()

    if lower_text.startswith("type "):

        content = text[5:].strip()

        if content:
            from app.tools.computer import execute_computer_action

            return execute_computer_action(
                "type",
                text=content
            )

    if lower_text in ["press enter", "hit enter"]:

        from app.tools.computer import execute_computer_action

        return execute_computer_action(
            "press_key",
            key="enter"
        )

    if lower_text in ["click", "click here", "left click"]:

        from app.tools.computer import execute_computer_action

        return execute_computer_action("click")

    if lower_text in [
        "screenshot",
        "take screenshot",
        "take a screenshot"
    ]:

        from app.tools.computer import execute_computer_action

        return execute_computer_action("screenshot")

    # ============================================================
    # AI MULTI-STEP COMPUTER TASK
    # ============================================================

    task_result = run_task(text)

    if task_result:
        return task_result

    return None