"""
LangChain-based memory management for conversation history.

Uses message history for efficient conversation context management.
"""
import logging
from typing import List, Dict, Any, Optional
from threading import Thread
import time

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.chat_history import InMemoryChatMessageHistory

from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


# ============================================================================
# IN-MEMORY CHAT HISTORY WITH CLEANUP
# ============================================================================

class MemoryStore:
    """Thread-safe memory store with automatic cleanup.

    Uses LangChain's InMemoryChatMessageHistory for session management.
    """

    def __init__(self, timeout_seconds: int = 3600, max_message_limit: int = 10):
        """Initialize memory store.

        Args:
            timeout_seconds: Session timeout in seconds (default: 1 hour)
            max_message_limit: Maximum messages to keep per session
        """
        self.sessions: Dict[str, InMemoryChatMessageHistory] = {}
        self.timestamps: Dict[str, float] = {}
        self.timeout = timeout_seconds
        self.max_message_limit = max_message_limit
        self._cleanup_task: Optional[Thread] = None

    def get_history(self, session_id: str) -> InMemoryChatMessageHistory:
        """Get or create chat history for a session."""
        if session_id not in self.sessions:
            self.sessions[session_id] = InMemoryChatMessageHistory()

        # Update timestamp
        self.timestamps[session_id] = time.time()
        return self.sessions[session_id]

    def add_message(self, session_id: str, role: str, content: str) -> None:
        """Add a message to the session history."""
        history = self.get_history(session_id)

        if role == "user":
            history.add_user_message(content)
        elif role == "assistant":
            history.add_ai_message(content)

    def get_history_as_dict(self, session_id: str) -> List[Dict[str, str]]:
        """Get conversation history as a list of dicts."""
        history = self.get_history(session_id)
        messages = history.messages

        result = []
        for msg in messages[-self.max_message_limit:]:  # Limit history size
            if isinstance(msg, HumanMessage):
                result.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                result.append({"role": "assistant", "content": msg.content})

        return result

    def get_messages_for_langchain(self, session_id: str) -> List[BaseMessage]:
        """Get messages in LangChain format for direct LLM calls."""
        history = self.get_history(session_id)
        return history.messages[-self.max_message_limit:]

    def cleanup_expired(self) -> int:
        """Remove expired sessions. Returns count of removed sessions."""
        now = time.time()
        expired = [
            sid for sid, timestamp in self.timestamps.items()
            if now - timestamp > self.timeout
        ]
        for sid in expired:
            del self.sessions[sid]
            del self.timestamps[sid]
        return len(expired)

    def start_cleanup_task(self) -> None:
        """Start background cleanup task."""
        if self._cleanup_task is None:
            self._cleanup_task = Thread(target=self._cleanup_loop, daemon=True)
            self._cleanup_task.start()

    def _cleanup_loop(self) -> None:
        """Run cleanup every 5 minutes."""
        while True:
            time.sleep(300)  # 5 minutes
            removed = self.cleanup_expired()
            if removed > 0:
                logger.info(f"Cleaned up {removed} expired sessions")

    def clear_session(self, session_id: str) -> None:
        """Clear a specific session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
        if session_id in self.timestamps:
            del self.timestamps[session_id]


# Global memory store instance
memory_store = MemoryStore(timeout_seconds=3600, max_message_limit=10)
memory_store.start_cleanup_task()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_conversation_summary(session_id: str) -> str:
    """Get a formatted summary of the conversation for context."""
    history = memory_store.get_history_as_dict(session_id)
    if not history:
        return ""

    summary_parts = []
    for msg in history[-5:]:  # Last 5 exchanges
        role = "User" if msg["role"] == "user" else "Assistant"
        content = msg["content"][:100] + ("..." if len(msg["content"]) > 100 else "")
        summary_parts.append(f"{role}: {content}")

    return "\n".join(summary_parts)


def build_messages_with_memory(
    query: str,
    session_id: Optional[str] = None,
    system_prompt: Optional[str] = None
) -> List[BaseMessage]:
    """Build LangChain messages including conversation history.

    Args:
        query: Current user query
        session_id: Optional session ID for history
        system_prompt: Optional system message

    Returns:
        List of LangChain BaseMessage objects
    """
    from langchain_core.messages import SystemMessage

    messages = []

    # Add system prompt if provided
    if system_prompt:
        messages.append(SystemMessage(content=system_prompt))

    # Add conversation history if session exists
    if session_id:
        history_messages = memory_store.get_messages_for_langchain(session_id)
        messages.extend(history_messages[:-2])  # Exclude last few to avoid redundancy

    # Add current query
    messages.append(HumanMessage(content=query))

    return messages


def format_context_with_history(
    query: str,
    session_id: Optional[str] = None,
    location_context: Optional[str] = None
) -> str:
    """Format query with conversation history for prompt injection.

    Args:
        query: Current user query
        session_id: Optional session ID for history
        location_context: Optional location information

    Returns:
        Formatted context string
    """
    parts = []

    # Add conversation summary if available
    if session_id:
        summary = get_conversation_summary(session_id)
        if summary:
            parts.append(f"## Previous Conversation:\n{summary}\n")

    # Add location context if available
    if location_context:
        parts.append(f"## Location Context:\n{location_context}\n")

    # Add current query
    parts.append(f"## Current Query:\n{query}")

    return "\n".join(parts)
