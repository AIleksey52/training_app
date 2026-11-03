from dataclasses import dataclass


@dataclass
class ProgramExercise:
    id: int
    program_id: int
    exercise_id: int
    position: int
    sets: int
    reps: int
    rest_seconds: int
    exercise_name: str | None = None  # служебное поле: название упражнения
