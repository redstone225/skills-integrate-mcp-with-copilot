import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

DB_PATH = Path(__file__).resolve().parent / "app.db"

CREATE_ACTIVITIES_TABLE = """
CREATE TABLE IF NOT EXISTS activities (
    name TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    schedule TEXT NOT NULL,
    max_participants INTEGER NOT NULL
);
"""

CREATE_PARTICIPANTS_TABLE = """
CREATE TABLE IF NOT EXISTS participants (
    activity_name TEXT NOT NULL,
    email TEXT NOT NULL,
    PRIMARY KEY (activity_name, email),
    FOREIGN KEY(activity_name) REFERENCES activities(name) ON DELETE CASCADE
);
"""

DEFAULT_ACTIVITIES = [
    {
        "name": "Chess Club",
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
    },
    {
        "name": "Programming Class",
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
    },
    {
        "name": "Gym Class",
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"],
    },
    {
        "name": "Soccer Team",
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"],
    },
    {
        "name": "Basketball Team",
        "description": "Practice and play basketball with the school team",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"],
    },
    {
        "name": "Art Club",
        "description": "Explore your creativity through painting and drawing",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"],
    },
    {
        "name": "Drama Club",
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"],
    },
    {
        "name": "Math Club",
        "description": "Solve challenging problems and participate in math competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"],
    },
    {
        "name": "Debate Team",
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "henry@mergington.edu"],
    },
]


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_connection() as conn:
        conn.execute(CREATE_ACTIVITIES_TABLE)
        conn.execute(CREATE_PARTICIPANTS_TABLE)
        conn.commit()

        existing = conn.execute("SELECT COUNT(*) as count FROM activities").fetchone()["count"]
        if existing == 0:
            for activity in DEFAULT_ACTIVITIES:
                conn.execute(
                    "INSERT INTO activities (name, description, schedule, max_participants) VALUES (?, ?, ?, ?)",
                    (activity["name"], activity["description"], activity["schedule"], activity["max_participants"]),
                )
                for email in activity["participants"]:
                    conn.execute(
                        "INSERT INTO participants (activity_name, email) VALUES (?, ?)",
                        (activity["name"], email),
                    )
            conn.commit()


def fetch_activities() -> Dict[str, Any]:
    with get_connection() as conn:
        rows = conn.execute("SELECT name, description, schedule, max_participants FROM activities ORDER BY name").fetchall()
        activities = {}
        for row in rows:
            participants = [
                r["email"]
                for r in conn.execute(
                    "SELECT email FROM participants WHERE activity_name = ? ORDER BY email",
                    (row["name"],),
                ).fetchall()
            ]
            activities[row["name"]] = {
                "description": row["description"],
                "schedule": row["schedule"],
                "max_participants": row["max_participants"],
                "participants": participants,
            }
        return activities


def add_participant(activity_name: str, email: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO participants (activity_name, email) VALUES (?, ?)",
            (activity_name, email),
        )
        conn.commit()


def remove_participant(activity_name: str, email: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM participants WHERE activity_name = ? AND email = ?",
            (activity_name, email),
        )
        conn.commit()


def activity_exists(activity_name: str) -> bool:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT 1 FROM activities WHERE name = ?",
            (activity_name,),
        ).fetchone()
        return row is not None


def participant_exists(activity_name: str, email: str) -> bool:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT 1 FROM participants WHERE activity_name = ? AND email = ?",
            (activity_name, email),
        ).fetchone()
        return row is not None
