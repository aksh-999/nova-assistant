from app.core.ai_brain import ask_ai
from app.core.router import route_command
from app.memory.memory import Memory


class NovaAssistant:

    def __init__(self):
        self.memory = Memory()

    def process(self, user_text):

        text = user_text.lower().strip()

        if text.startswith("remember that "):
            memory_text = user_text[len("remember that "):].strip()
            self.memory.remember("general", memory_text)
            return "I'll remember that."

        if (
            "what am i working on" in text
            or "what project am i building" in text
            or "what am i building" in text
        ):
            memories = self.memory.get_all()

            if not memories:
                return "I don't have anything saved yet."

            latest_memory = memories[0][1]
            return f"You told me: {latest_memory}"

        tool_response = route_command(user_text)

        if tool_response:
            return tool_response

        return ask_ai(user_text)

    def remember(self, key, value):
        self.memory.remember(key, value)

    def recall(self, key):
        return self.memory.recall(key)

    def close(self):
        self.memory.close()