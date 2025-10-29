"""
LiveKit Voice Tutor Agent
==================================
A voice tutor agent using Deepgram for speech recognition.
Teaches students about specific topics in a conversational style.
"""

from dotenv import load_dotenv
from livekit import agents
from livekit.agents import Agent, AgentSession, RunContext
from livekit.agents.llm import function_tool
from livekit.plugins import openai, deepgram, silero
import os
import asyncio

# Load environment variables
load_dotenv()

class TutorAgent(Agent):
    """Voice tutor agent that teaches students about specific topics."""

    def __init__(self, topic: str, subject: str, style: str = "friendly and encouraging"):
        super().__init__(
            instructions=f"""You are a highly knowledgeable tutor teaching a real-time voice session with a student. Your goal is to teach the student about the topic and subject.

Tutor Guidelines:
- Stick to the given topic - {topic} and subject - {subject} and teach the student about it.
- Keep the conversation flowing smoothly while maintaining control.
- From time to time make sure that the student is following you and understands you.
- Break down the topic into smaller parts and teach the student one part at a time.
- Keep your style of conversation {style}.
- Keep your responses short, like in a real voice conversation.
- Do not include any special characters in your responses - this is a voice conversation.
- Ask questions to check understanding and engage the student.
- Provide clear explanations and examples when needed.
- Adapt your pace based on student responses."""
        )
        
        self.topic = topic
        self.subject = subject
        self.style = style
        self.current_subtopic = None
        self.conversation_history = []

    @function_tool
    async def check_understanding(self, context: RunContext, question: str = None) -> str:
        """Check if the student understands the current concept.
        
        Args:
            question: Optional specific question to ask the student
        """
        if question:
            return f"Let me check your understanding. {question}"
        else:
            return "Does that make sense so far? Please feel free to ask any questions."

    @function_tool
    async def move_to_next_subtopic(self, context: RunContext, subtopic: str) -> str:
        """Move to the next subtopic in the lesson.
        
        Args:
            subtopic: The next subtopic to teach
        """
        self.current_subtopic = subtopic
        self.conversation_history.append(f"Moved to subtopic: {subtopic}")
        return f"Great! Now let's move on to {subtopic}. This is an important part of our topic."

    @function_tool
    async def provide_example(self, context: RunContext, concept: str) -> str:
        """Provide a concrete example to illustrate a concept.
        
        Args:
            concept: The concept that needs an example
        """
        return f"Let me give you an example to illustrate {concept}. This should help make it clearer."

    @function_tool
    async def summarize_key_points(self, context: RunContext) -> str:
        """Summarize the key points covered so far."""
        return "Let me quickly summarize the key points we've covered so far. This will help reinforce your learning."

    @function_tool
    async def adjust_pace(self, context: RunContext, slower: bool = True) -> str:
        """Adjust the teaching pace based on student needs.
        
        Args:
            slower: Whether to slow down (True) or speed up (False) the pace
        """
        if slower:
            return "I notice you might need more time with this. Let me slow down and go through this more carefully."
        else:
            return "You're grasping this quickly! Let me move a bit faster since you're following along well."

async def entrypoint(ctx: agents.JobContext):
    """Entry point for the tutor agent."""
    
    # Get topic and subject from environment or use defaults
    topic = os.getenv("TUTOR_TOPIC", "artificial intelligence")
    subject = os.getenv("TUTOR_SUBJECT", "machine learning basics")
    style = os.getenv("TUTOR_STYLE", "friendly and encouraging")
    
    # Configure session with all required components
    session = AgentSession(
        stt=deepgram.STT(
            model="nova-2",
            api_key=os.getenv("DEEPGRAM_API_KEY")
        ),
        llm=openai.LLM(model=os.getenv("LLM_CHOICE", "gpt-4.1-mini")),
        tts=openai.TTS(voice="echo"),
        vad=silero.VAD.load(),
    )

    # Start the session with the tutor agent
    tutor = TutorAgent(topic=topic, subject=subject, style=style)
    await session.start(
        room=ctx.room,
        agent=tutor
    )

    # Generate initial greeting and lesson introduction
    await session.generate_reply(
        instructions=f"""Begin the tutoring session by:
1. Warmly greeting the student
2. Introducing today's topic: {topic} in the subject of {subject}
3. Briefly outlining what you'll cover
4. Asking if the student has any prior knowledge or specific questions
Keep it conversational and engaging."""
    )
    
if __name__ == "__main__":
    # Run the agent
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
