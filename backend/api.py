from livekit.agents import function_tool, Agent, RunContext
from typing import Annotated, Optional
import logging
import random
from db_driver import DatabaseDriver, Subtopic

logger = logging.getLogger("tutor")
logger.setLevel(logging.INFO)

DB = DatabaseDriver()

class TutorAgent(Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_subtopic: Optional[Subtopic] = None
        self.conversation_history: list[str] = []
        self.student_understanding_score: float = 0.5  # 0-1 scale
        self.teaching_pace: str = "normal"  # slow, normal, fast
        self.topics_covered: list[str] = []
        self.questions_asked: int = 0

    @function_tool()
    async def check_understanding(
        self,
        context: RunContext,
        question: Annotated[str, dict(description="Optional specific question to ask")] = None,
    ) -> str:
        self.questions_asked += 1
        if question:
            return f"Let me check your understanding. {question}"

        # Vary the phrasing to keep it natural
        prompts = [
            "Does that make sense so far? Feel free to ask any questions.",
            "Can you explain what we just covered in your own words?",
            "What questions do you have about this?",
            "Is this clear, or should I explain it differently?",
        ]
        return random.choice(prompts)

    @function_tool()
    async def move_to_next_subtopic(
        self,
        context: RunContext,
        subtopic: Annotated[str, dict(description="The next subtopic to teach")]
    ) -> str:
        # Track previously covered topics
        if self.current_subtopic:
            self.topics_covered.append(self.current_subtopic.subtopic)

        self.current_subtopic = Subtopic(id=0, topic="", subtopic=subtopic, content="")
        self.conversation_history.append(f"Moved to subtopic: {subtopic}")

        # Provide context-aware transition
        if self.topics_covered:
            return f"Great work on {self.topics_covered[-1]}! Now let's explore {subtopic}."
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
            self.teaching_pace = "slow"
            self.student_understanding_score = max(0, self.student_understanding_score - 0.1)
            return "I notice you might need more time. Let me slow down and break this into smaller steps."
        else:
            self.teaching_pace = "fast"
            self.student_understanding_score = min(1, self.student_understanding_score + 0.1)
            return "You're catching on quickly! Let's pick up the pace and dive deeper."

    @function_tool()
    async def provide_encouragement(
        self,
        context: RunContext,
        achievement: Annotated[str, dict(description="What to celebrate")] = ""
    ) -> str:
        """Provide positive reinforcement and encouragement"""
        phrases = [
            "Great thinking! Keep it up.",
            "You're doing excellent work!",
            "That's exactly right!",
            "I love how you're connecting these ideas!",
            "You're making fantastic progress!",
        ]
        base = random.choice(phrases)
        if achievement:
            return f"{base} You just {achievement}!"
        return base

    @function_tool()
    async def address_confusion(
        self,
        context: RunContext,
        topic: Annotated[str, dict(description="Topic causing confusion")]
    ) -> str:
        """Address student confusion with a different approach"""
        return f"I see {topic} might be confusing. Let me explain it a different way with a clear example."

    @function_tool()
    async def create_practice_problem(
        self,
        context: RunContext,
        topic: Annotated[str, dict(description="Topic to practice")]
    ) -> str:
        """Generate a practice problem for the student"""
        return f"Let's practice what we learned about {topic}. Here's a problem to work through together."

    def has_subtopic(self) -> bool:
        return self.current_subtopic is not None

    def get_progress_stats(self) -> dict:
        """Get learning progress statistics"""
        return {
            "topics_covered": len(self.topics_covered),
            "questions_asked": self.questions_asked,
            "understanding_score": round(self.student_understanding_score * 100),
            "teaching_pace": self.teaching_pace
        }
