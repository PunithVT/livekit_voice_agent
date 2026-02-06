"""
Voice command recognition and execution system
Allows hands-free control of the tutoring session
"""
from typing import Dict, Callable, Optional, List
from dataclasses import dataclass
import re


@dataclass
class VoiceCommand:
    """Voice command model"""
    command: str
    patterns: List[str]
    description: str
    category: str
    example: str
    handler: Optional[Callable] = None


class VoiceCommandSystem:
    """Process and execute voice commands"""

    def __init__(self):
        self.commands = self._initialize_commands()

    def _initialize_commands(self) -> Dict[str, VoiceCommand]:
        """Initialize all available voice commands"""
        commands = {
            # Session control
            "pause": VoiceCommand(
                command="pause",
                patterns=[
                    r"\b(pause|stop|wait)\b",
                    r"\bhang on\b",
                    r"\bgive me (a )?second\b"
                ],
                description="Pause the tutoring session",
                category="control",
                example="Pause the session"
            ),

            "resume": VoiceCommand(
                command="resume",
                patterns=[
                    r"\b(resume|continue|go on)\b",
                    r"\blets? continue\b",
                    r"\bkeep going\b"
                ],
                description="Resume the tutoring session",
                category="control",
                example="Continue please"
            ),

            "repeat": VoiceCommand(
                command="repeat",
                patterns=[
                    r"\b(repeat|say (that )?again)\b",
                    r"\bcan you repeat\b",
                    r"\bwhat did you say\b",
                    r"\bdidnt (catch|hear) that\b"
                ],
                description="Repeat the last explanation",
                category="control",
                example="Can you repeat that?"
            ),

            # Pace control
            "slow_down": VoiceCommand(
                command="slow_down",
                patterns=[
                    r"\b(slow down|go slower|too fast)\b",
                    r"\byou['']?re going too (fast|quick)\b",
                    r"\bslower please\b"
                ],
                description="Slow down the teaching pace",
                category="pace",
                example="Slow down please"
            ),

            "speed_up": VoiceCommand(
                command="speed_up",
                patterns=[
                    r"\b(speed up|go faster|too slow)\b",
                    r"\bfaster please\b",
                    r"\byou['']?re going too slow\b"
                ],
                description="Speed up the teaching pace",
                category="pace",
                example="Can you go faster?"
            ),

            # Content navigation
            "example": VoiceCommand(
                command="example",
                patterns=[
                    r"\bgive (me )?(an )?example\b",
                    r"\bshow (me )?(an )?example\b",
                    r"\bcan (you|i) (have|get|see) (an )?example\b"
                ],
                description="Request an example",
                category="content",
                example="Give me an example"
            ),

            "summary": VoiceCommand(
                command="summary",
                patterns=[
                    r"\b(summarize|summary|recap)\b",
                    r"\bwhat did we (cover|learn)\b",
                    r"\bsummarize (what|everything) we (covered|learned)\b"
                ],
                description="Get a summary of what was covered",
                category="content",
                example="Summarize what we learned"
            ),

            "next_topic": VoiceCommand(
                command="next_topic",
                patterns=[
                    r"\b(next (topic|subject)|move on|skip)\b",
                    r"\bcan we move (on|forward)\b",
                    r"\blets? (do|try) (the )?next (one|topic)\b"
                ],
                description="Move to the next topic",
                category="navigation",
                example="Next topic please"
            ),

            "previous_topic": VoiceCommand(
                command="previous_topic",
                patterns=[
                    r"\b(previous|last|go back) (topic|subject)\b",
                    r"\bgo back to (the )?(last|previous)\b"
                ],
                description="Go back to the previous topic",
                category="navigation",
                example="Go back to the previous topic"
            ),

            # Help and clarification
            "confused": VoiceCommand(
                command="confused",
                patterns=[
                    r"\b(im? |i am )?(confused|lost|dont understand)\b",
                    r"\bthis (is |makes )no sense\b",
                    r"\bi dont get (it|this)\b"
                ],
                description="Signal confusion and request clarification",
                category="help",
                example="I'm confused"
            ),

            "clarify": VoiceCommand(
                command="clarify",
                patterns=[
                    r"\b(clarify|explain (again|more|better))\b",
                    r"\bcan you (clarify|elaborate)\b",
                    r"\bexplain (that|this) differently\b"
                ],
                description="Request clarification or different explanation",
                category="help",
                example="Can you clarify that?"
            ),

            "hint": VoiceCommand(
                command="hint",
                patterns=[
                    r"\b(give (me )?a hint|need a hint)\b",
                    r"\bcan (you|i) (have|get) a hint\b"
                ],
                description="Request a hint for a problem",
                category="help",
                example="Give me a hint"
            ),

            # Practice and testing
            "practice": VoiceCommand(
                command="practice",
                patterns=[
                    r"\b(practice|quiz|test) (me|question)\b",
                    r"\bgive me (a )?(practice |quiz )?question\b",
                    r"\blets? practice\b"
                ],
                description="Request a practice question",
                category="practice",
                example="Give me a practice question"
            ),

            "answer": VoiceCommand(
                command="answer",
                patterns=[
                    r"\b(show|tell|give) (me )?(the )?answer\b",
                    r"\bwhat['']?s the answer\b",
                    r"\bshow solution\b"
                ],
                description="Show the answer to a problem",
                category="practice",
                example="Show me the answer"
            ),

            # Progress and stats
            "progress": VoiceCommand(
                command="progress",
                patterns=[
                    r"\b(my |show )?(progress|stats|statistics)\b",
                    r"\bhow am i doing\b",
                    r"\bwhat['']?s my (score|progress)\b"
                ],
                description="Show learning progress",
                category="stats",
                example="Show my progress"
            ),

            # Session management
            "end_session": VoiceCommand(
                command="end_session",
                patterns=[
                    r"\b(end|finish|stop) (the )?session\b",
                    r"\b(im? |i am )done\b",
                    r"\blets? (finish|end|stop)\b"
                ],
                description="End the tutoring session",
                category="control",
                example="End the session"
            ),
        }

        return commands

    def recognize_command(self, text: str) -> Optional[str]:
        """
        Recognize a voice command from text

        Args:
            text: Transcribed speech text

        Returns:
            Command name if recognized, None otherwise
        """
        text_lower = text.lower().strip()

        # Check each command's patterns
        for command_name, command in self.commands.items():
            for pattern in command.patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    return command_name

        return None

    def execute_command(
        self,
        command_name: str,
        context: Dict = None
    ) -> Dict:
        """
        Execute a recognized command

        Args:
            command_name: Name of the command to execute
            context: Optional context data

        Returns:
            Result dictionary with action and response
        """
        if command_name not in self.commands:
            return {
                "success": False,
                "error": f"Unknown command: {command_name}"
            }

        command = self.commands[command_name]

        # Map commands to actions
        actions = {
            "pause": {"action": "pause_session", "response": "Session paused. Say 'continue' when ready."},
            "resume": {"action": "resume_session", "response": "Continuing..."},
            "repeat": {"action": "repeat_last", "response": "Let me repeat that..."},
            "slow_down": {"action": "adjust_pace", "params": {"slower": True}, "response": "Slowing down..."},
            "speed_up": {"action": "adjust_pace", "params": {"slower": False}, "response": "Speeding up..."},
            "example": {"action": "provide_example", "response": "Here's an example..."},
            "summary": {"action": "summarize", "response": "Let me summarize what we've covered..."},
            "next_topic": {"action": "next_topic", "response": "Moving to the next topic..."},
            "previous_topic": {"action": "previous_topic", "response": "Going back to the previous topic..."},
            "confused": {"action": "address_confusion", "response": "Let me explain this differently..."},
            "clarify": {"action": "clarify", "response": "Let me clarify that..."},
            "hint": {"action": "give_hint", "response": "Here's a hint..."},
            "practice": {"action": "generate_practice", "response": "Here's a practice question..."},
            "answer": {"action": "show_answer", "response": "The answer is..."},
            "progress": {"action": "show_progress", "response": "Here's your progress..."},
            "end_session": {"action": "end_session", "response": "Ending session. Great work today!"},
        }

        result = actions.get(command_name, {"action": "unknown", "response": "Command not implemented"})
        result["success"] = True
        result["command"] = command_name

        return result

    def get_available_commands(self, category: Optional[str] = None) -> List[VoiceCommand]:
        """
        Get list of available commands

        Args:
            category: Optional category filter

        Returns:
            List of VoiceCommand objects
        """
        commands = list(self.commands.values())

        if category:
            commands = [c for c in commands if c.category == category]

        return commands

    def get_command_help(self) -> str:
        """
        Get formatted help text for all commands

        Returns:
            Formatted help string
        """
        help_text = "Available Voice Commands:\n\n"

        # Group by category
        categories = {}
        for command in self.commands.values():
            if command.category not in categories:
                categories[command.category] = []
            categories[command.category].append(command)

        # Format each category
        for category, cmds in sorted(categories.items()):
            help_text += f"**{category.upper()}**\n"
            for cmd in cmds:
                help_text += f"- {cmd.description}: '{cmd.example}'\n"
            help_text += "\n"

        return help_text


# Singleton instance
voice_commands = VoiceCommandSystem()
