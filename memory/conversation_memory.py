"""
memory/conversation_memory.py
-----------------------------

Manages conversation history for FinAssist AI.

Current Storage:
    - In-memory

Future Upgrade:
    - SQLite
    - ChromaDB
    - Redis
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict


@dataclass
class ConversationMemory:
    """
    Stores conversation history for the current session.
    """

    history: List[Dict] = field(default_factory=list)

    def add_message(
        self,
        role: str,
        content: str
    ) -> None:
        """
        Store a message.

        Parameters
        ----------
        role
            "user" or "assistant"

        content
            Message text
        """

        self.history.append(
            {
                "role": role,
                "content": content,
                "timestamp": datetime.now()
            }
        )

    def get_history(self) -> List[Dict]:
        """
        Return conversation history.
        """

        return self.history

    def clear(self) -> None:
        """
        Clear all conversation history.
        """

        self.history.clear()

    def last_message(self):
        """
        Return last conversation.
        """

        if not self.history:
            return None

        return self.history[-1]

    def as_text(self) -> str:
        """
        Convert conversation into text.

        Useful for LLM prompts.
        """

        lines = []

        for message in self.history:

            lines.append(
                f"{message['role'].capitalize()}: {message['content']}"
            )

        return "\n".join(lines)


# Singleton instance used across the application
conversation_memory = ConversationMemory()