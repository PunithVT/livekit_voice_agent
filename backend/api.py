from livekit.agents import function_tool, Agent, RunContext
from typing import Annotated, Optional
import logging
from db_driver import DatabaseDriver, Subtopic

logger = logging.getLogger("tutor")
logger.setLevel(logging.INFO)

DB = DatabaseDriver()

class TutorAgent(Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_subtopic: Optional[Subtopic] = None
        self.conversation_history: list[str] = []

    @function_tool()
    async def check_understanding(
        self,
        context: RunContext,
        question: Annotated[str, dict(description="Optional specific question to ask")] = None,
    ) -> str:
        if question:
            return f"Let me check your understanding. {question}"
        return "Does that make sense so far? Feel free to ask any questions."

    @function_tool()
    async def move_to_next_subtopic(
        self,
        context: RunContext,
        subtopic: Annotated[str, dict(description="The next subtopic to teach")]
    ) -> str:
        self.current_subtopic = Subtopic(id=0, topic="", subtopic=subtopic, content="")
        self.conversation_history.append(f"Moved to subtopic: {subtopic}")
        return f"Great! Now let's move on to {subtopic}."

    @function_tool()
    async def provide_example(
        self,
        context: RunContext,
        concept: Annotated[str, dict(description="The concept that needs an example")]
    ) -> str:
        return f"Let me give you an example to illustrate {concept}."

    @function_tool()
    async def summarize_key_points(
        self,
        context: RunContext
    ) -> str:
        return "Here is a quick summary of the key points we've covered so far."

    @function_tool()
    async def adjust_pace(
        self,
        context: RunContext,
        slower: Annotated[bool, dict(description="True to slow down, False to speed up")] = True
    ) -> str:
        if slower:
            return "I notice you might need more time. Let me slow down a bit."
        return "You're catching on quickly! I'll speed up a little."

    def has_subtopic(self) -> bool:
        return self.current_subtopic is not None
