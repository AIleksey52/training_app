from models.exercise import Exercise
from repositories import exercise_repository, program_exercise_repository
from services.errors import ServiceError
from services.validators import optional_text, require_text


def get_all_exercises() -> list[Exercise]:
    return exercise_repository.get_all()


def get_exercise(exercise_id: int) -> Exercise:
    exercise = exercise_repository.get_by_id(exercise_id)
    if not exercise:
        raise ServiceError("Упражнение не найдено")
    return exercise


def _check_unique_name(name: str, exclude_id: int | None = None):
    for e in exercise_repository.get_all():
        if e.name.lower() == name.lower() and e.exercise_id != exclude_id:
            raise ServiceError("Упражнение с таким названием уже существует")


def create_exercise(name: str, description: str | None) -> int:
    name = require_text(name, "Название")
    description = optional_text(description)
    _check_unique_name(name)
    return exercise_repository.create(name, description)


def update_exercise(exercise_id: int, name: str, description: str | None):
    get_exercise(exercise_id)
    name = require_text(name, "Название")
    description = optional_text(description)
    _check_unique_name(name, exclude_id=exercise_id)
    exercise_repository.update(exercise_id, name, description)


def delete_exercise(exercise_id: int):
    get_exercise(exercise_id)
    used = program_exercise_repository.count_by_exercise(exercise_id)
    if used:
        raise ServiceError(f"Упражнение используется в программах ({used} шт.) — удалить нельзя")
    exercise_repository.delete(exercise_id)
