from config import TRAINER_ROLE_ID
from models.difficulty_level import DifficultyLevel
from models.program import Program
from models.program_exercise import ProgramExercise
from models.user import User
from repositories import (difficulty_level_repository, exercise_repository,
                          program_exercise_repository, program_repository,
                          user_repository)
from services.errors import ServiceError
from services.validators import optional_text, require_int, require_text

WORK_SECONDS_PER_SET = 40  # средняя длительность одного подхода для оценки времени


# ---------- чтение ----------

def get_levels() -> list[DifficultyLevel]:
    return difficulty_level_repository.get_all()


def get_all_programs() -> list[Program]:
    return program_repository.get_all()


def get_programs_by_level(level_id: int) -> list[Program]:
    if not difficulty_level_repository.get_by_id(level_id):
        raise ServiceError("Уровень сложности не найден")
    return program_repository.get_by_level(level_id)


def search_programs(text: str) -> list[Program]:
    text = require_text(text, "Строка поиска")
    return program_repository.search_by_name(text)


def get_program(program_id: int) -> Program:
    program = program_repository.get_by_id(program_id)
    if not program:
        raise ServiceError("Программа не найдена")
    return program


def get_program_exercises(program_id: int) -> list[ProgramExercise]:
    get_program(program_id)
    return program_exercise_repository.get_by_program(program_id)


# ---------- проверки ----------

def _check_trainer(user: User):
    if user.role_id != TRAINER_ROLE_ID:
        raise ServiceError("Действие доступно только тренеру")


def _check_owner(user: User, program: Program):
    _check_trainer(user)
    if program.trainer_id != user.user_id:
        raise ServiceError("Изменять программу может только её автор")


def _validate_program(name, description, duration_weeks, level_id):
    name = require_text(name, "Название")
    description = optional_text(description)
    duration_weeks = require_int(duration_weeks, "Длительность (нед.)", 1, 52)
    level_id = require_int(level_id, "Уровень", 1, 10**9)
    if not difficulty_level_repository.get_by_id(level_id):
        raise ServiceError("Уровень сложности не найден")
    return name, description, duration_weeks, level_id


def _validate_load(sets, reps, rest_seconds):
    return (require_int(sets, "Подходы", 1, 20),
            require_int(reps, "Повторения", 1, 200),
            require_int(rest_seconds, "Отдых (сек)", 0, 600))


# ---------- программы (CRUD) ----------

def create_program(user: User, name, description, duration_weeks, level_id) -> int:
    _check_trainer(user)
    if not user_repository.get_by_id(user.user_id):
        raise ServiceError("Тренер не найден")
    name, description, duration_weeks, level_id = _validate_program(
        name, description, duration_weeks, level_id)
    for p in program_repository.get_by_trainer(user.user_id):
        if p.name.lower() == name.lower():
            raise ServiceError("У вас уже есть программа с таким названием")
    return program_repository.create(name, description, duration_weeks, level_id, user.user_id)


def update_program(user: User, program_id: int, name, description, duration_weeks, level_id):
    program = get_program(program_id)
    _check_owner(user, program)
    name, description, duration_weeks, level_id = _validate_program(
        name, description, duration_weeks, level_id)
    program_repository.update(program_id, name, description, duration_weeks, level_id)


def delete_program(user: User, program_id: int):
    program = get_program(program_id)
    _check_owner(user, program)
    program_repository.delete(program_id)


# ---------- упражнения внутри программы ----------

def add_exercise_to_program(user: User, program_id: int, exercise_id: int,
                            sets, reps, rest_seconds) -> int:
    program = get_program(program_id)
    _check_owner(user, program)
    if not exercise_repository.get_by_id(exercise_id):
        raise ServiceError("Упражнение не найдено")
    sets, reps, rest_seconds = _validate_load(sets, reps, rest_seconds)
    position = program_exercise_repository.get_next_position(program_id)
    return program_exercise_repository.create(program_id, exercise_id, position,
                                              sets, reps, rest_seconds)


def _get_item_of_owner(user: User, item_id: int) -> ProgramExercise:
    item = program_exercise_repository.get_by_id(item_id)
    if not item:
        raise ServiceError("Упражнение в программе не найдено")
    _check_owner(user, get_program(item.program_id))
    return item


def update_program_exercise(user: User, item_id: int, sets, reps, rest_seconds):
    _get_item_of_owner(user, item_id)
    sets, reps, rest_seconds = _validate_load(sets, reps, rest_seconds)
    program_exercise_repository.update(item_id, sets, reps, rest_seconds)


def remove_exercise_from_program(user: User, item_id: int):
    _get_item_of_owner(user, item_id)
    program_exercise_repository.delete(item_id)


# ---------- тренировка спортсмена ----------

def build_workout(program_id: int, sets_override=None, rest_override=None):
    """Готовит план тренировки. Спортсмен может задать своё число подходов
    и время отдыха (use case «Выбор количества подходов и времени»).
    Возвращает (список упражнений, оценка длительности в минутах)."""
    items = get_program_exercises(program_id)
    if not items:
        raise ServiceError("В программе пока нет упражнений")
    if sets_override not in (None, ""):
        sets_override = require_int(sets_override, "Подходы", 1, 20)
    else:
        sets_override = None
    if rest_override not in (None, ""):
        rest_override = require_int(rest_override, "Отдых (сек)", 0, 600)
    else:
        rest_override = None

    total_seconds = 0
    for item in items:
        if sets_override is not None:
            item.sets = sets_override
        if rest_override is not None:
            item.rest_seconds = rest_override
        total_seconds += item.sets * WORK_SECONDS_PER_SET + (item.sets - 1) * item.rest_seconds
    return items, round(total_seconds / 60)
