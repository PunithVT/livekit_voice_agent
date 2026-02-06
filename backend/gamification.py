"""
Gamification system for learning motivation
Includes points, badges, achievements, and streaks
"""
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import json


@dataclass
class Achievement:
    """Achievement/Badge model"""
    id: str
    name: str
    description: str
    icon: str
    points: int
    rarity: str  # common, rare, epic, legendary
    unlocked_at: Optional[str] = None


@dataclass
class LearningStreak:
    """Daily learning streak tracker"""
    user_id: str
    current_streak: int
    longest_streak: int
    last_activity: str
    total_sessions: int


class GamificationEngine:
    """Gamification system for student engagement"""

    # Achievement definitions
    ACHIEVEMENTS = {
        # Beginner achievements
        "first_session": Achievement(
            id="first_session",
            name="First Steps",
            description="Complete your first tutoring session",
            icon="🎯",
            points=10,
            rarity="common"
        ),
        "curious_mind": Achievement(
            id="curious_mind",
            name="Curious Mind",
            description="Ask 10 questions in a session",
            icon="❓",
            points=15,
            rarity="common"
        ),
        "quick_learner": Achievement(
            id="quick_learner",
            name="Quick Learner",
            description="Complete 5 topics in one session",
            icon="⚡",
            points=25,
            rarity="rare"
        ),

        # Streak achievements
        "on_fire": Achievement(
            id="on_fire",
            name="On Fire!",
            description="Maintain a 7-day learning streak",
            icon="🔥",
            points=50,
            rarity="rare"
        ),
        "unstoppable": Achievement(
            id="unstoppable",
            name="Unstoppable",
            description="Maintain a 30-day learning streak",
            icon="💪",
            points=200,
            rarity="epic"
        ),

        # Mastery achievements
        "problem_solver": Achievement(
            id="problem_solver",
            name="Problem Solver",
            description="Solve 20 practice problems correctly",
            icon="🧩",
            points=75,
            rarity="rare"
        ),
        "master_learner": Achievement(
            id="master_learner",
            name="Master Learner",
            description="Achieve 90% understanding score in 10 sessions",
            icon="🎓",
            points=150,
            rarity="epic"
        ),

        # Time-based achievements
        "marathon": Achievement(
            id="marathon",
            name="Marathon Learner",
            description="Study for 2 hours straight",
            icon="⏱️",
            points=100,
            rarity="epic"
        ),
        "night_owl": Achievement(
            id="night_owl",
            name="Night Owl",
            description="Complete a session after 10 PM",
            icon="🦉",
            points=20,
            rarity="common"
        ),
        "early_bird": Achievement(
            id="early_bird",
            name="Early Bird",
            description="Complete a session before 7 AM",
            icon="🌅",
            points=20,
            rarity="common"
        ),

        # Legendary achievements
        "polymath": Achievement(
            id="polymath",
            name="Polymath",
            description="Master 10 different subjects",
            icon="🌟",
            points=500,
            rarity="legendary"
        ),
        "teaching_legend": Achievement(
            id="teaching_legend",
            name="Teaching Legend",
            description="Complete 100 tutoring sessions",
            icon="👑",
            points=1000,
            rarity="legendary"
        ),
    }

    # Point values for actions
    POINTS = {
        "session_complete": 10,
        "question_asked": 2,
        "correct_answer": 5,
        "topic_completed": 15,
        "practice_completed": 20,
        "daily_login": 5,
        "perfect_session": 50,  # 100% understanding score
    }

    def __init__(self):
        self.user_data = {}  # In-memory storage (should use database)

    def award_points(self, user_id: str, action: str, multiplier: float = 1.0) -> Dict:
        """
        Award points for an action

        Args:
            user_id: User identifier
            action: Action key from POINTS
            multiplier: Point multiplier (for bonuses)

        Returns:
            Dictionary with points awarded and new total
        """
        if action not in self.POINTS:
            return {"error": f"Unknown action: {action}"}

        points = int(self.POINTS[action] * multiplier)

        # Get or create user data
        if user_id not in self.user_data:
            self.user_data[user_id] = {
                "total_points": 0,
                "level": 1,
                "achievements": [],
                "actions": []
            }

        # Award points
        self.user_data[user_id]["total_points"] += points
        self.user_data[user_id]["actions"].append({
            "action": action,
            "points": points,
            "timestamp": datetime.utcnow().isoformat()
        })

        # Check for level up
        old_level = self.user_data[user_id]["level"]
        new_level = self._calculate_level(self.user_data[user_id]["total_points"])
        leveled_up = new_level > old_level

        if leveled_up:
            self.user_data[user_id]["level"] = new_level

        return {
            "points_awarded": points,
            "total_points": self.user_data[user_id]["total_points"],
            "level": new_level,
            "leveled_up": leveled_up,
            "action": action
        }

    def _calculate_level(self, total_points: int) -> int:
        """Calculate user level based on total points"""
        # Level formula: level = sqrt(points / 100) + 1
        import math
        return int(math.sqrt(total_points / 100)) + 1

    def check_achievements(
        self,
        user_id: str,
        session_data: Dict
    ) -> List[Achievement]:
        """
        Check if user unlocked any new achievements

        Args:
            user_id: User identifier
            session_data: Session statistics

        Returns:
            List of newly unlocked achievements
        """
        if user_id not in self.user_data:
            return []

        user_achievements = set(self.user_data[user_id].get("achievements", []))
        newly_unlocked = []

        # Check each achievement
        for achievement_id, achievement in self.ACHIEVEMENTS.items():
            if achievement_id in user_achievements:
                continue  # Already unlocked

            # Check unlock conditions
            if self._check_achievement_conditions(achievement_id, user_id, session_data):
                achievement.unlocked_at = datetime.utcnow().isoformat()
                newly_unlocked.append(achievement)
                self.user_data[user_id]["achievements"].append(achievement_id)

                # Award achievement points
                self.user_data[user_id]["total_points"] += achievement.points

        return newly_unlocked

    def _check_achievement_conditions(
        self,
        achievement_id: str,
        user_id: str,
        session_data: Dict
    ) -> bool:
        """Check if conditions are met for an achievement"""
        # This is simplified - should check against database in production

        conditions = {
            "first_session": lambda: session_data.get("session_count", 0) >= 1,
            "curious_mind": lambda: session_data.get("questions_asked", 0) >= 10,
            "quick_learner": lambda: session_data.get("topics_completed", 0) >= 5,
            "problem_solver": lambda: session_data.get("problems_solved", 0) >= 20,
            "master_learner": lambda: (
                session_data.get("high_score_sessions", 0) >= 10 and
                session_data.get("avg_understanding", 0) >= 90
            ),
        }

        check_func = conditions.get(achievement_id)
        if check_func:
            try:
                return check_func()
            except Exception:
                return False

        return False

    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get top users by points"""
        sorted_users = sorted(
            self.user_data.items(),
            key=lambda x: x[1]["total_points"],
            reverse=True
        )

        return [
            {
                "user_id": user_id,
                "points": data["total_points"],
                "level": data["level"],
                "rank": idx + 1
            }
            for idx, (user_id, data) in enumerate(sorted_users[:limit])
        ]

    def get_user_stats(self, user_id: str) -> Optional[Dict]:
        """Get user's gamification stats"""
        if user_id not in self.user_data:
            return None

        data = self.user_data[user_id]

        # Calculate next level requirements
        current_level = data["level"]
        points_for_next = (current_level ** 2) * 100
        progress_to_next = (data["total_points"] / points_for_next) * 100

        return {
            "user_id": user_id,
            "total_points": data["total_points"],
            "level": current_level,
            "next_level_progress": min(progress_to_next, 100),
            "achievements_count": len(data["achievements"]),
            "achievements": [
                self.ACHIEVEMENTS[aid] for aid in data["achievements"]
                if aid in self.ACHIEVEMENTS
            ],
            "recent_actions": data["actions"][-10:]  # Last 10 actions
        }

    def update_streak(self, user_id: str) -> LearningStreak:
        """Update user's learning streak"""
        # This should interact with database in production
        now = datetime.utcnow()

        if user_id not in self.user_data:
            self.user_data[user_id] = {
                "streak": {
                    "current": 1,
                    "longest": 1,
                    "last_activity": now.isoformat(),
                    "total_sessions": 1
                }
            }
        else:
            streak_data = self.user_data[user_id].get("streak", {
                "current": 0,
                "longest": 0,
                "last_activity": None,
                "total_sessions": 0
            })

            last_activity = datetime.fromisoformat(streak_data["last_activity"]) if streak_data["last_activity"] else None

            if last_activity:
                days_diff = (now - last_activity).days

                if days_diff == 0:
                    # Same day, just increment sessions
                    pass
                elif days_diff == 1:
                    # Next day, continue streak
                    streak_data["current"] += 1
                else:
                    # Streak broken
                    streak_data["current"] = 1

            else:
                streak_data["current"] = 1

            # Update longest streak
            streak_data["longest"] = max(streak_data["longest"], streak_data["current"])
            streak_data["last_activity"] = now.isoformat()
            streak_data["total_sessions"] += 1

            self.user_data[user_id]["streak"] = streak_data

        return LearningStreak(
            user_id=user_id,
            current_streak=self.user_data[user_id]["streak"]["current"],
            longest_streak=self.user_data[user_id]["streak"]["longest"],
            last_activity=self.user_data[user_id]["streak"]["last_activity"],
            total_sessions=self.user_data[user_id]["streak"]["total_sessions"]
        )


# Singleton instance
gamification = GamificationEngine()
