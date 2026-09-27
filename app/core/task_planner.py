import json
import re

from app.core.ai_brain import ask_ai
from app.tools.computer import execute_computer_action


# ============================================================
# AI TASK PLANNER
# ============================================================

def plan_task(user_text):

    prompt = f"""
You are Nova's computer-action planner.

Convert the user's request into a JSON ARRAY.

Allowed actions:

{{"action":"open_app","app_name":"notepad"}}

{{"action":"open_website","url":"https://example.com"}}

{{"action":"type","text":"Hello Nova"}}

{{"action":"press_key","key":"enter"}}

{{"action":"hotkey","keys":["ctrl","s"]}}

{{"action":"screenshot"}}

{{"action":"move_mouse","x":500,"y":300}}

{{"action":"click"}}

IMPORTANT:
- The final answer MUST be a JSON ARRAY.
- Every action MUST be a separate JSON OBJECT.
- Never put multiple actions inside one object.
- Never use shell commands.
- Never delete files.
- Never shut down or restart the computer.
- Never perform destructive actions.
- If this is not a computer-control request, return [].
- Return ONLY JSON. No explanation.

Example:

User:
Open Notepad and type Hello Nova

Correct:
[
  {{"action":"open_app","app_name":"notepad"}},
  {{"action":"type","text":"Hello Nova"}}
]

User request:
{user_text}
"""

    response = ask_ai(user_text=prompt)

    if not response:
        return []

    response = re.sub(
        r"```json|```",
        "",
        response,
        flags=re.IGNORECASE
    ).strip()

    try:

        actions = json.loads(response)

        if not isinstance(actions, list):
            return []

        valid_actions = {
            "open_app",
            "open_website",
            "type",
            "press_key",
            "hotkey",
            "screenshot",
            "move_mouse",
            "click"
        }

        safe_actions = []

        for action in actions:

            if not isinstance(action, dict):
                continue

            if action.get("action") in valid_actions:
                safe_actions.append(action)

        return safe_actions

    except json.JSONDecodeError:

        print("[Nova Planner] Invalid JSON from AI:")
        print(response)

        return []

# ============================================================
# EXECUTE PLANNED TASK
# ============================================================

def execute_task(actions):

    results = []

    for action in actions:

        if not isinstance(action, dict):
            continue

        action_type = action.get("action")

        if not action_type:
            continue

        kwargs = {
            key: value
            for key, value in action.items()
            if key != "action"
        }

        result = execute_computer_action(
            action_type,
            **kwargs
        )

        if result:
            results.append(result)

    return results


# ============================================================
# PLAN + EXECUTE
# ============================================================

def run_task(user_text):

    actions = plan_task(
        user_text
    )

    if not actions:
        return None

    print(
        "[Nova Planner] Planned actions:"
    )

    print(actions)

    results = execute_task(
        actions
    )

    if not results:
        return None

    return " ".join(results)