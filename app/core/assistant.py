from app.core.ai_brain import ask_ai
from app.core.router import route_command
from app.memory.memory import Memory


class NovaAssistant:

    def __init__(self):
        self.memory = Memory()

    # ============================================================
    # SMART MEMORY CONTEXT
    # ============================================================

    def get_memory_context(self, user_text, limit=5):

        # --------------------------------------------------------
        # 1. Try the complete user query first
        # --------------------------------------------------------

        memories = self.memory.search(
            user_text,
            limit=limit
        )

        if memories:

            lines = []

            for memory in memories:

                lines.append(
                    f"- {memory['value']}"
                )

            return "\n".join(lines)

        # --------------------------------------------------------
        # 2. If no direct match, search useful keywords
        # --------------------------------------------------------

        words = [
            word.strip(".,!?")
            for word in user_text.lower().split()
            if len(word.strip(".,!?")) >= 5
        ]

        collected = []
        seen_ids = set()

        for word in words:

            results = self.memory.search(
                word,
                limit=limit
            )

            for memory in results:

                if memory["id"] not in seen_ids:

                    collected.append(memory)

                    seen_ids.add(
                        memory["id"]
                    )

        # --------------------------------------------------------
        # 3. Nothing relevant found
        # --------------------------------------------------------

        if not collected:
            return None

        # --------------------------------------------------------
        # 4. Important memories first
        # --------------------------------------------------------

        collected.sort(
            key=lambda memory: (
                memory["importance"],
                memory["id"]
            ),
            reverse=True
        )

        # --------------------------------------------------------
        # 5. Build AI context
        # --------------------------------------------------------

        lines = []

        for memory in collected[:limit]:

            lines.append(
                f"- {memory['value']}"
            )

        return "\n".join(lines)

    # ============================================================
    # PROCESS USER INPUT
    # ============================================================

    def process(self, user_text):

        text = user_text.lower().strip()

        # ========================================================
        # REMEMBER
        # ========================================================

        if text.startswith("remember that "):

            memory_text = user_text[
                len("remember that "):
            ].strip()

            self.memory.remember(
                key="general",
                value=memory_text,
                category="general",
                importance=2
            )

            return "I'll remember that."

        # ========================================================
        # FORGET
        # ========================================================

        if text.startswith("forget that "):

            memory_text = user_text[
                len("forget that "):
            ].strip()

            memories = self.memory.search(
                memory_text
            )

            if not memories:

                return (
                    "I couldn't find anything "
                    "matching that memory."
                )

            deleted = 0

            for memory in memories:

                if (
                    memory["value"].lower()
                    == memory_text.lower()
                ):

                    if self.memory.delete(
                        memory["id"]
                    ):
                        deleted += 1

            if deleted:

                return "I've forgotten that."

            return (
                "I couldn't find an exact "
                "memory matching that."
            )

        # ========================================================
        # WHAT DO YOU REMEMBER?
        # ========================================================

        if (
            "what do you remember about me" in text
            or "what do you remember" in text
            or "show my memories" in text
        ):

            memories = self.memory.get_all()

            if not memories:

                return (
                    "I don't have any memories "
                    "saved yet."
                )

            important = [
                memory
                for memory in memories
                if memory["importance"] >= 2
            ]

            selected = (
                important
                if important
                else memories
            )

            lines = []

            for memory in selected[:10]:

                lines.append(
                    f"- {memory['value']}"
                )

            return (
                "Here's what I remember:\n"
                + "\n".join(lines)
            )

        # ========================================================
        # WHAT AM I WORKING ON?
        # ========================================================

        if (
            "what am i working on" in text
            or "what project am i building" in text
            or "what am i building" in text
        ):

            memories = self.memory.search(
                "project",
                limit=10
            )

            if memories:

                return (
                    f"You told me: "
                    f"{memories[0]['value']}"
                )

            memories = self.memory.get_all()

            if not memories:

                return (
                    "I don't have anything "
                    "saved yet."
                )

            return (
                f"You told me: "
                f"{memories[0]['value']}"
            )

        # ========================================================
        # SEARCH MEMORY
        # ========================================================

        if text.startswith(
            "search memory for "
        ):

            query = user_text[
                len("search memory for "):
            ].strip()

            results = self.memory.search(
                query
            )

            if not results:

                return (
                    "I couldn't find anything "
                    "matching that."
                )

            lines = []

            for memory in results[:10]:

                lines.append(
                    f"- {memory['value']}"
                )

            return (
                "I found these memories:\n"
                + "\n".join(lines)
            )

        # ========================================================
        # COMPUTER TOOLS
        # ========================================================

        tool_response = route_command(
            user_text
        )

        if tool_response:

            return tool_response

        # ========================================================
        # SMART MEMORY RETRIEVAL
        # ========================================================

        memory_context = self.get_memory_context(
            user_text
        )

        # ========================================================
        # AI
        # ========================================================

        return ask_ai(
            user_text,
            memory_context
        )

    # ============================================================
    # PUBLIC MEMORY METHODS
    # ============================================================

    def remember(
        self,
        key,
        value,
        category="general",
        importance=1
    ):

        return self.memory.remember(
            key=key,
            value=value,
            category=category,
            importance=importance
        )

    def recall(self, key):

        return self.memory.recall(
            key
        )

    def search_memory(
        self,
        query,
        limit=10
    ):

        return self.memory.search(
            query,
            limit
        )

    def forget(self, key):

        return self.memory.forget(
            key
        )

    # ============================================================
    # CLOSE
    # ============================================================

    def close(self):

        self.memory.close()