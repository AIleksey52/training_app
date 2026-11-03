"""Экраны, общие для тренера и спортсмена."""
from services import program_service
from services.errors import ServiceError
from ui.helpers import ask, ask_id, print_table


def show_programs(programs):
    print_table(["ID", "Название", "Уровень", "Недель", "Тренер"],
                [[p.program_id, p.name, p.level_name, p.duration_weeks, p.trainer_name]
                 for p in programs])


def show_levels():
    print_table(["ID", "Уровень"], [[l.level_id, l.name] for l in program_service.get_levels()])


def show_program_details(program_id: int):
    program = program_service.get_program(program_id)
    print(f"\n=== {program.name} ===")
    print(f"Уровень: {program.level_name} | Длительность: {program.duration_weeks} нед. "
          f"| Тренер: {program.trainer_name}")
    if program.description:
        print(f"Описание: {program.description}")
    print()
    items = program_service.get_program_exercises(program_id)
    print_table(["№ записи", "Поз.", "Упражнение", "Подходы", "Повторы", "Отдых, с"],
                [[i.id, i.position, i.exercise_name, i.sets, i.reps, i.rest_seconds]
                 for i in items])


def programs_by_level_screen():
    show_levels()
    level_id = ask_id("ID уровня")
    if level_id is not None:
        show_programs(program_service.get_programs_by_level(level_id))


def search_screen():
    show_programs(program_service.search_programs(ask("Часть названия")))


def program_details_screen():
    program_id = ask_id("ID программы")
    if program_id is not None:
        show_program_details(program_id)


def run_safely(action):
    """Вызывает действие и показывает ошибки бизнес-логики, не роняя программу."""
    try:
        action()
    except ServiceError as e:
        print(f"Ошибка: {e}")
