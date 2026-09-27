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

        if not collected:
            return None

        collected.sort(
            key=lambda memory: (
                memory["importance"],
                memory["id"]
            ),
            reverse=True
        )

        lines = []

        for memory in collected[:limit]:

            lines.append(
                f"- {memory['value']}"
            )

        return "\n".join(lines)

    # ============================================================
    # RECENT CONVERSATION
    # ============================================================

    def get_conversation_context(self, limit=10):

        messages = self.memory.get_recent_messages(
            limit=limit
        )

        if not messages:
            return None

        lines = []

        for message in messages:

            role = message["role"].capitalize()

            lines.append(
                f"{role}: {message['content']}"
            )

        return "\n".join(lines)

    # ============================================================
    # COMBINED AI CONTEXT
    # ============================================================

    def get_ai_context(self, user_text):

        memory_context = self.get_memory_context(
            user_text
        )

        conversation_context = (
            self.get_conversation_context(
                limit=10
            )
        )

        sections = []

        if memory_context:

            sections.append(
                "LONG-TERM MEMORY:\n"
                + memory_context
            )

        if conversation_context:

            sections.append(
                "RECENT CONVERSATION:\n"
                + conversation_context
            )

        if not sections:
            return None

        return "\n\n".join(sections)

    # ============================================================
    # AUTOMATIC MEMORY DETECTION
    # ============================================================

    def detect_automatic_memory(self, user_text):

        text = user_text.lower().strip()

        memory_patterns = [
            "my name is ",
            "i am ",
            "i'm ",
            "i use ",
            "i prefer ",
            "i like ",
            "i love ",
            "i live in ",
            "i study ",
            "i'm studying ",
            "i am studying ",
            "i work on ",
            "i'm working on ",
            "i am working on ",
            "i am building ",
            "i'm building ",
            "my startup is ",
            "my project is ",
        ]

        for pattern in memory_patterns:

            if text.startswith(pattern):

                value = user_text[
                    len(pattern):
                ].strip()

                if not value:
                    return

                # Ignore very short or conversational statements
                if len(value) < 3:
                    return

                # Avoid saving questions
                if "?" in value:
                    return

                # Avoid saving temporary actions
                temporary_words = [
                    "today",
                    "now",
                    "right now",
                    "currently",
                    "just",
                    "going to",
                ]

                if value.lower() in temporary_words:
                    return

                # Determine category
                category = "general"

                if (
                    "startup" in text
                    or "project" in text
                    or "building" in text
                    or "working on" in text
                ):
                    category = "project"

                elif (
                    "study" in text
                    or "studying" in text
                ):
                    category = "education"

                elif (
                    "prefer" in text
                    or "like" in text
                    or "love" in text
                ):
                    category = "preference"

                elif "name" in text:
                    category = "personal"

                elif "use" in text:
                    category = "technology"

                elif "live" in text:
                    category = "location"

                # Important personal facts get higher priority
                importance = 1

                if (
                    category == "personal"
                    or category == "project"
                ):
                    importance = 2

                self.memory.remember(
                    key=category,
                    value=user_text,
                    category=category,
                    importance=importance
                )

                return

    # ============================================================
    # PROCESS USER INPUT
    # ============================================================

    def process(self, user_text):

        text = user_text.lower().strip()

        # ========================================================
        # CLEAR CONVERSATION
        # ========================================================

        clear_commands = [
            "clear our conversation",
            "clear conversation",
            "clear chat",
            "clear chat history",
            "forget this conversation",
            "forget our conversation",
            "start a new conversation",
            "start new conversation",
            "new conversation"
        ]

        if text in clear_commands:

            self.memory.clear_conversation()

            response = (
                "Conversation cleared. "
                "Your saved memories are still safe."
            )

            self.memory.add_message(
                role="assistant",
                content=response
            )

            return response

        # ========================================================
        # SAVE USER MESSAGE
        # ========================================================

        self.memory.add_message(
            role="user",
            content=user_text
        )

        # ========================================================
        # EXPLICIT REMEMBER
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

            response = "I'll remember that."

            self.memory.add_message(
                role="assistant",
                content=response
            )

            return response

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

                response = (
                    "I couldn't find anything "
                    "matching that memory."
                )

                self.memory.add_message(
                    role="assistant",
                    content=response
                )

                return response

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

                response = "I've forgotten that."

            else:

                response = (
                    "I couldn't find an exact "
                    "memory matching that."
                )

            self.memory.add_message(
                role="assistant",
                content=response
            )

            return response

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

                response = (
                    "I don't have any memories "
                    "saved yet."
                )

                self.memory.add_message(
                    role="assistant",
                    content=response
                )

                return response

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

            response = (
                "Here's what I remember:\n"
                + "\n".join(lines)
            )

            self.memory.add_message(
                role="assistant",
                content=response
            )

            return response

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

                response = (
                    f"You told me: "
                    f"{memories[0]['value']}"
                )

                self.memory.add_message(
                    role="assistant",
                    content=response
                )

                return response

            memories = self.memory.get_all()

            if not memories:

                response = (
                    "I don't have anything "
                    "saved yet."
                )

                self.memory.add_message(
                    role="assistant",
                    content=response
                )

                return response

            response = (
                f"You told me: "
                f"{memories[0]['value']}"
            )

            self.memory.add_message(
                role="assistant",
                content=response
            )

            return response

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

                response = (
                    "I couldn't find anything "
                    "matching that."
                )

                self.memory.add_message(
                    role="assistant",
                    content=response
                )

                return response

            lines = []

            for memory in results[:10]:

                lines.append(
                    f"- {memory['value']}"
                )

            response = (
                "I found these memories:\n"
                + "\n".join(lines)
            )

            self.memory.add_message(
                role="assistant",
                content=response
            )

            return response

        # ========================================================
        # AUTOMATIC MEMORY
        # ========================================================

        self.detect_automatic_memory(
            user_text
        )

        # ========================================================
        # COMPUTER TOOLS
        # ========================================================

        tool_response = route_command(
            user_text
        )

        if tool_response:

            self.memory.add_message(
                role="assistant",
                content=tool_response
            )

            return tool_response

        # ========================================================
        # AI CONTEXT
        # ========================================================

        ai_context = self.get_ai_context(
            user_text
        )

        # ========================================================
        # AI
        # ========================================================

        response = ask_ai(
            user_text,
            ai_context
        )

        # ========================================================
        # SAVE AI RESPONSE
        # ========================================================

        self.memory.add_message(
            role="assistant",
            content=response
        )

        return response

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