"""Tests for TutorAgent class"""
import pytest
from unittest.mock import Mock, AsyncMock
from api import TutorAgent
from db_driver import Subtopic


@pytest.mark.unit
class TestTutorAgent:
    """Test TutorAgent class"""

    @pytest.fixture
    def tutor_agent(self):
        """Create a TutorAgent instance"""
        mock_model = Mock()
        return TutorAgent(model=mock_model)

    @pytest.mark.asyncio
    async def test_check_understanding_with_question(self, tutor_agent):
        """Test check_understanding with a question"""
        mock_context = Mock()
        result = await tutor_agent.check_understanding(
            mock_context,
            question="Can you explain derivatives?"
        )

        assert "Can you explain derivatives?" in result
        assert "check your understanding" in result

    @pytest.mark.asyncio
    async def test_check_understanding_without_question(self, tutor_agent):
        """Test check_understanding without a question"""
        mock_context = Mock()
        result = await tutor_agent.check_understanding(mock_context)

        assert "make sense" in result.lower()
        assert "questions" in result.lower()

    @pytest.mark.asyncio
    async def test_move_to_next_subtopic(self, tutor_agent):
        """Test moving to next subtopic"""
        mock_context = Mock()
        result = await tutor_agent.move_to_next_subtopic(
            mock_context,
            subtopic="Linear Equations"
        )

        assert "Linear Equations" in result
        assert tutor_agent.current_subtopic is not None
        assert tutor_agent.current_subtopic.subtopic == "Linear Equations"
        assert len(tutor_agent.conversation_history) == 1

    @pytest.mark.asyncio
    async def test_provide_example(self, tutor_agent):
        """Test providing an example"""
        mock_context = Mock()
        result = await tutor_agent.provide_example(
            mock_context,
            concept="Pythagorean theorem"
        )

        assert "Pythagorean theorem" in result
        assert "example" in result.lower()

    @pytest.mark.asyncio
    async def test_summarize_key_points(self, tutor_agent):
        """Test summarizing key points"""
        mock_context = Mock()
        result = await tutor_agent.summarize_key_points(mock_context)

        assert "summary" in result.lower()
        assert "key points" in result.lower()

    @pytest.mark.asyncio
    async def test_adjust_pace_slower(self, tutor_agent):
        """Test adjusting pace to slower"""
        mock_context = Mock()
        result = await tutor_agent.adjust_pace(mock_context, slower=True)

        assert "slow down" in result.lower()

    @pytest.mark.asyncio
    async def test_adjust_pace_faster(self, tutor_agent):
        """Test adjusting pace to faster"""
        mock_context = Mock()
        result = await tutor_agent.adjust_pace(mock_context, slower=False)

        assert "speed up" in result.lower() or "quickly" in result.lower()

    def test_has_subtopic_false(self, tutor_agent):
        """Test has_subtopic when no subtopic is set"""
        assert tutor_agent.has_subtopic() is False

    def test_has_subtopic_true(self, tutor_agent):
        """Test has_subtopic when subtopic is set"""
        tutor_agent.current_subtopic = Subtopic(
            id=1,
            topic="Test",
            subtopic="Test Sub",
            content="Test content"
        )
        assert tutor_agent.has_subtopic() is True

    def test_conversation_history_tracking(self, tutor_agent):
        """Test conversation history tracking"""
        assert len(tutor_agent.conversation_history) == 0

        # Add some history through move_to_next_subtopic
        mock_context = Mock()
        import asyncio
        asyncio.run(tutor_agent.move_to_next_subtopic(mock_context, "Topic 1"))
        asyncio.run(tutor_agent.move_to_next_subtopic(mock_context, "Topic 2"))

        assert len(tutor_agent.conversation_history) == 2
        assert "Topic 1" in tutor_agent.conversation_history[0]
        assert "Topic 2" in tutor_agent.conversation_history[1]
