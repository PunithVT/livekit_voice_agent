"""Tests for database driver"""
import pytest
from db_driver import DatabaseDriver, Subtopic


@pytest.mark.unit
class TestDatabaseDriver:
    """Test DatabaseDriver class"""

    def test_init_creates_database(self, test_db):
        """Test database initialization"""
        assert test_db is not None
        assert test_db.db_path == ":memory:"

    def test_create_subtopic(self, test_db, sample_subtopic):
        """Test creating a subtopic"""
        subtopic = test_db.create_subtopic(
            topic=sample_subtopic["topic"],
            subtopic=sample_subtopic["subtopic"],
            content=sample_subtopic["content"]
        )

        assert isinstance(subtopic, Subtopic)
        assert subtopic.id > 0
        assert subtopic.topic == sample_subtopic["topic"]
        assert subtopic.subtopic == sample_subtopic["subtopic"]
        assert subtopic.content == sample_subtopic["content"]

    def test_get_subtopic(self, test_db, sample_subtopic):
        """Test retrieving a subtopic"""
        # Create a subtopic first
        created = test_db.create_subtopic(
            topic=sample_subtopic["topic"],
            subtopic=sample_subtopic["subtopic"],
            content=sample_subtopic["content"]
        )

        # Retrieve it
        retrieved = test_db.get_subtopic(created.id)

        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.topic == created.topic

    def test_get_nonexistent_subtopic(self, test_db):
        """Test retrieving a non-existent subtopic"""
        subtopic = test_db.get_subtopic(99999)
        assert subtopic is None

    def test_list_subtopics(self, test_db, sample_subtopic):
        """Test listing subtopics by topic"""
        # Create multiple subtopics
        test_db.create_subtopic(
            topic="Mathematics",
            subtopic="Algebra",
            content="Algebra content"
        )
        test_db.create_subtopic(
            topic="Mathematics",
            subtopic="Geometry",
            content="Geometry content"
        )
        test_db.create_subtopic(
            topic="Physics",
            subtopic="Mechanics",
            content="Mechanics content"
        )

        # List mathematics subtopics
        math_subtopics = test_db.list_subtopics("Mathematics")
        assert len(math_subtopics) == 2

        # List physics subtopics
        physics_subtopics = test_db.list_subtopics("Physics")
        assert len(physics_subtopics) == 1

    def test_list_subtopics_empty(self, test_db):
        """Test listing subtopics when none exist"""
        subtopics = test_db.list_subtopics("NonexistentTopic")
        assert len(subtopics) == 0
        assert isinstance(subtopics, list)


@pytest.mark.unit
class TestSubtopicDataclass:
    """Test Subtopic dataclass"""

    def test_subtopic_creation(self):
        """Test creating a Subtopic instance"""
        subtopic = Subtopic(
            id=1,
            topic="Test",
            subtopic="Test Subtopic",
            content="Test content"
        )

        assert subtopic.id == 1
        assert subtopic.topic == "Test"
        assert subtopic.subtopic == "Test Subtopic"
        assert subtopic.content == "Test content"

    def test_subtopic_equality(self):
        """Test Subtopic equality"""
        subtopic1 = Subtopic(1, "Test", "Sub", "Content")
        subtopic2 = Subtopic(1, "Test", "Sub", "Content")

        assert subtopic1 == subtopic2
