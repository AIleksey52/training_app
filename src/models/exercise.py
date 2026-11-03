from dataclasses import dataclass


@dataclass
class Exercise:
    exercise_id: int
    name: str
    description: str | None = None
