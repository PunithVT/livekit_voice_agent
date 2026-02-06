"""
AI-powered quiz generator for interactive learning
Generates quizzes, flashcards, and practice problems from topics
"""
from typing import List, Dict, Optional
from dataclasses import dataclass
import random


@dataclass
class QuizQuestion:
    """Quiz question model"""
    id: str
    question: str
    question_type: str  # multiple_choice, true_false, short_answer, fill_blank
    options: Optional[List[str]] = None
    correct_answer: str = ""
    explanation: str = ""
    difficulty: str = "medium"  # easy, medium, hard
    points: int = 10


@dataclass
class Quiz:
    """Quiz model"""
    id: str
    title: str
    description: str
    topic: str
    questions: List[QuizQuestion]
    total_points: int
    time_limit_minutes: Optional[int] = None


@dataclass
class QuizResult:
    """Quiz result model"""
    quiz_id: str
    user_id: str
    score: int
    max_score: int
    percentage: float
    correct_answers: int
    total_questions: int
    time_taken_seconds: int
    answers: Dict[str, str]


class QuizGenerator:
    """Generate quizzes from learning content"""

    # Question templates
    TEMPLATES = {
        "definition": "What is {concept}?",
        "example": "Which of the following is an example of {concept}?",
        "comparison": "What is the difference between {concept1} and {concept2}?",
        "application": "How would you apply {concept} in {context}?",
        "analysis": "Why is {concept} important for {context}?",
        "synthesis": "How does {concept} relate to {concept2}?",
    }

    def __init__(self):
        self.quizzes = {}  # Store generated quizzes

    def generate_quiz(
        self,
        topic: str,
        num_questions: int = 10,
        difficulty: str = "medium",
        question_types: Optional[List[str]] = None
    ) -> Quiz:
        """
        Generate a quiz for a topic

        Args:
            topic: Topic to generate quiz for
            num_questions: Number of questions
            difficulty: Difficulty level
            question_types: Types of questions to include

        Returns:
            Generated Quiz object
        """
        if question_types is None:
            question_types = ["multiple_choice", "true_false", "short_answer"]

        questions = []
        quiz_id = f"quiz_{random.randint(1000, 9999)}"

        for i in range(num_questions):
            q_type = random.choice(question_types)
            question = self._generate_question(
                topic=topic,
                question_type=q_type,
                difficulty=difficulty,
                question_id=f"{quiz_id}_q{i+1}"
            )
            questions.append(question)

        total_points = sum(q.points for q in questions)

        quiz = Quiz(
            id=quiz_id,
            title=f"{topic} Quiz",
            description=f"Test your knowledge of {topic}",
            topic=topic,
            questions=questions,
            total_points=total_points,
            time_limit_minutes=num_questions * 2  # 2 minutes per question
        )

        self.quizzes[quiz_id] = quiz
        return quiz

    def _generate_question(
        self,
        topic: str,
        question_type: str,
        difficulty: str,
        question_id: str
    ) -> QuizQuestion:
        """Generate a single question"""

        if question_type == "multiple_choice":
            return self._generate_multiple_choice(topic, difficulty, question_id)
        elif question_type == "true_false":
            return self._generate_true_false(topic, difficulty, question_id)
        elif question_type == "short_answer":
            return self._generate_short_answer(topic, difficulty, question_id)
        elif question_type == "fill_blank":
            return self._generate_fill_blank(topic, difficulty, question_id)
        else:
            # Default to multiple choice
            return self._generate_multiple_choice(topic, difficulty, question_id)

    def _generate_multiple_choice(
        self,
        topic: str,
        difficulty: str,
        question_id: str
    ) -> QuizQuestion:
        """Generate multiple choice question"""

        # This is a template - in production, use OpenAI API to generate real questions
        question_text = f"Which statement best describes {topic}?"

        options = [
            f"Option A about {topic}",
            f"Option B about {topic}",
            f"Option C about {topic}",
            f"Option D about {topic}",
        ]

        points = {"easy": 5, "medium": 10, "hard": 15}.get(difficulty, 10)

        return QuizQuestion(
            id=question_id,
            question=question_text,
            question_type="multiple_choice",
            options=options,
            correct_answer=options[0],
            explanation=f"The correct answer explains {topic} comprehensively.",
            difficulty=difficulty,
            points=points
        )

    def _generate_true_false(
        self,
        topic: str,
        difficulty: str,
        question_id: str
    ) -> QuizQuestion:
        """Generate true/false question"""

        question_text = f"{topic} is essential for understanding the broader concept."

        return QuizQuestion(
            id=question_id,
            question=question_text,
            question_type="true_false",
            options=["True", "False"],
            correct_answer="True",
            explanation=f"This statement about {topic} is true because...",
            difficulty=difficulty,
            points=5
        )

    def _generate_short_answer(
        self,
        topic: str,
        difficulty: str,
        question_id: str
    ) -> QuizQuestion:
        """Generate short answer question"""

        question_text = f"Explain the main concept of {topic} in your own words."

        return QuizQuestion(
            id=question_id,
            question=question_text,
            question_type="short_answer",
            options=None,
            correct_answer=f"A comprehensive explanation of {topic}",
            explanation="A good answer should cover the key aspects...",
            difficulty=difficulty,
            points=15
        )

    def _generate_fill_blank(
        self,
        topic: str,
        difficulty: str,
        question_id: str
    ) -> QuizQuestion:
        """Generate fill-in-the-blank question"""

        question_text = f"The key principle of {topic} is ___________."

        return QuizQuestion(
            id=question_id,
            question=question_text,
            question_type="fill_blank",
            options=None,
            correct_answer="the fundamental concept",
            explanation="The blank should be filled with...",
            difficulty=difficulty,
            points=10
        )

    def grade_quiz(
        self,
        quiz_id: str,
        user_id: str,
        answers: Dict[str, str],
        time_taken_seconds: int
    ) -> QuizResult:
        """
        Grade a completed quiz

        Args:
            quiz_id: Quiz identifier
            user_id: User identifier
            answers: User's answers (question_id -> answer)
            time_taken_seconds: Time taken to complete

        Returns:
            QuizResult with score and feedback
        """
        if quiz_id not in self.quizzes:
            raise ValueError(f"Quiz {quiz_id} not found")

        quiz = self.quizzes[quiz_id]
        score = 0
        correct_count = 0

        for question in quiz.questions:
            user_answer = answers.get(question.id, "").strip().lower()
            correct_answer = question.correct_answer.strip().lower()

            # Simple grading (in production, use more sophisticated comparison)
            if question.question_type == "multiple_choice":
                if user_answer == correct_answer:
                    score += question.points
                    correct_count += 1
            elif question.question_type == "true_false":
                if user_answer == correct_answer:
                    score += question.points
                    correct_count += 1
            elif question.question_type == "short_answer":
                # Partial credit for short answer (would use NLP in production)
                if correct_answer in user_answer or user_answer in correct_answer:
                    score += question.points * 0.8
                    correct_count += 0.8
            elif question.question_type == "fill_blank":
                if user_answer == correct_answer or user_answer in correct_answer:
                    score += question.points
                    correct_count += 1

        percentage = (score / quiz.total_points) * 100 if quiz.total_points > 0 else 0

        return QuizResult(
            quiz_id=quiz_id,
            user_id=user_id,
            score=int(score),
            max_score=quiz.total_points,
            percentage=round(percentage, 2),
            correct_answers=int(correct_count),
            total_questions=len(quiz.questions),
            time_taken_seconds=time_taken_seconds,
            answers=answers
        )

    def generate_flashcards(
        self,
        topic: str,
        num_cards: int = 10
    ) -> List[Dict[str, str]]:
        """
        Generate flashcards for spaced repetition

        Args:
            topic: Topic for flashcards
            num_cards: Number of flashcards

        Returns:
            List of flashcard dictionaries
        """
        flashcards = []

        for i in range(num_cards):
            flashcards.append({
                "id": f"card_{i+1}",
                "front": f"Key concept {i+1} of {topic}",
                "back": f"Explanation of concept {i+1}",
                "topic": topic,
                "difficulty": random.choice(["easy", "medium", "hard"])
            })

        return flashcards

    def get_quiz(self, quiz_id: str) -> Optional[Quiz]:
        """Get a quiz by ID"""
        return self.quizzes.get(quiz_id)

    def list_quizzes(self, topic: Optional[str] = None) -> List[Quiz]:
        """List all quizzes, optionally filtered by topic"""
        if topic:
            return [q for q in self.quizzes.values() if q.topic == topic]
        return list(self.quizzes.values())


# Singleton instance
quiz_generator = QuizGenerator()
