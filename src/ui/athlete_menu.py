from services import program_service
from ui import auth
from ui.common import (program_details_screen, programs_by_level_screen,
                       run_safely, search_screen, show_programs)
from ui.helpers import ask, ask_id, pause, print_table


def start_workout_screen():
    program_id = ask_id("ID программы")
    if program_id is None:
        return
    program = program_service.get_program(program_id)
    print("Можно задать свои параметры (Enter — как в программе).")
    sets = ask("Подходов на каждое упражнение", "")
    rest = ask("Отдых между подходами, сек", "")
    items, minutes = program_service.build_workout(program_id, sets, rest)

    print(f"\n=== Тренировка «{program.name}» — примерно {minutes} мин ===")
    print_table(["Поз.", "Упражнение", "Подходы", "Повторы", "Отдых, с"],
                [[i.position, i.exercise_name, i.sets, i.reps, i.rest_seconds] for i in items])
    if input("\nНачать тренировку? (д/н): ").strip().lower() not in ("д", "y", "да"):
        return
    for n, item in enumerate(items, start=1):
        print(f"\nУпражнение {n}/{len(items)}: {item.exercise_name}")
        for s in range(1, item.sets + 1):
            input(f"  Подход {s}/{item.sets}: {item.reps} повт. — Enter, когда закончите")
            if s < item.sets and item.rest_seconds:
                print(f"  Отдых {item.rest_seconds} сек")
    print("\nТренировка завершена! Отличная работа.")


def athlete_menu(user):
    while True:
        print(f"\n===== Спортсмен ({user.login}) =====")
        print("1. Все тренировочные программы")
        print("2. Программы по уровню сложности")
        print("3. Поиск программы по названию")
        print("4. Подробнее о программе")
        print("5. Начать тренировку")
        print("6. Сменить пароль")
        print("0. Выйти из аккаунта")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            run_safely(lambda: show_programs(program_service.get_all_programs()))
        elif choice == "2":
            run_safely(programs_by_level_screen)
        elif choice == "3":
            run_safely(search_screen)
        elif choice == "4":
            run_safely(program_details_screen)
        elif choice == "5":
            run_safely(start_workout_screen)
        elif choice == "6":
            auth.change_password(user)
        elif choice == "0":
            break
        else:
            print("Нет такого пункта")
            continue
        pause()
