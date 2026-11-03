from services import exercise_service, program_service, user_service
from ui import auth
from ui.common import (program_details_screen, programs_by_level_screen,
                       run_safely, search_screen, show_levels,
                       show_program_details, show_programs)
from ui.helpers import ask, ask_id, pause, print_table


# ---------- упражнения ----------

def show_exercises():
    print_table(["ID", "Название", "Описание"],
                [[e.exercise_id, e.name, e.description]
                 for e in exercise_service.get_all_exercises()])


def create_exercise_screen():
    new_id = exercise_service.create_exercise(ask("Название"), ask("Описание (можно пусто)"))
    print(f"Упражнение добавлено (ID {new_id}).")


def update_exercise_screen():
    exercise_id = ask_id("ID упражнения")
    if exercise_id is None:
        return
    e = exercise_service.get_exercise(exercise_id)
    exercise_service.update_exercise(exercise_id, ask("Название", e.name),
                                     ask("Описание", e.description or ""))
    print("Упражнение изменено.")


def delete_exercise_screen():
    exercise_id = ask_id("ID упражнения")
    if exercise_id is not None:
        exercise_service.delete_exercise(exercise_id)
        print("Упражнение удалено.")


def exercises_menu():
    while True:
        print("\n----- Упражнения -----")
        print("1. Список упражнений")
        print("2. Добавить упражнение")
        print("3. Изменить упражнение")
        print("4. Удалить упражнение")
        print("0. Назад")
        choice = input("Выберите действие: ").strip()
        actions = {"1": show_exercises, "2": create_exercise_screen,
                   "3": update_exercise_screen, "4": delete_exercise_screen}
        if choice == "0":
            break
        if choice in actions:
            run_safely(actions[choice])
            pause()
        else:
            print("Нет такого пункта")


# ---------- программы ----------

def create_program_screen(user):
    name = ask("Название")
    description = ask("Описание (можно пусто)")
    weeks = ask("Длительность, недель")
    show_levels()
    level_id = ask("ID уровня")
    new_id = program_service.create_program(user, name, description, weeks, level_id)
    print(f"Программа создана (ID {new_id}). Добавьте в неё упражнения в пункте «Состав программы».")


def update_program_screen(user):
    program_id = ask_id("ID программы")
    if program_id is None:
        return
    p = program_service.get_program(program_id)
    print("Enter — оставить текущее значение.")
    name = ask("Название", p.name)
    description = ask("Описание", p.description or "")
    weeks = ask("Длительность, недель", p.duration_weeks)
    show_levels()
    level_id = ask("ID уровня", p.level_id)
    program_service.update_program(user, program_id, name, description, weeks, level_id)
    print("Программа изменена.")


def delete_program_screen(user):
    program_id = ask_id("ID программы")
    if program_id is None:
        return
    p = program_service.get_program(program_id)
    if input(f"Удалить «{p.name}» вместе с упражнениями? (д/н): ").strip().lower() in ("д", "y", "да"):
        program_service.delete_program(user, program_id)
        print("Программа удалена.")


def program_content_menu(user):
    program_id = ask_id("ID программы")
    if program_id is None:
        return
    program_service.get_program(program_id)  # проверка существования
    while True:
        show_program_details(program_id)
        print("\n1. Добавить упражнение")
        print("2. Изменить подходы / повторы / отдых")
        print("3. Убрать упражнение из программы")
        print("0. Назад")
        choice = input("Выберите действие: ").strip()
        if choice == "0":
            break
        if choice == "1":
            def add():
                show_exercises()
                exercise_id = ask_id("ID упражнения")
                if exercise_id is None:
                    return
                program_service.add_exercise_to_program(
                    user, program_id, exercise_id,
                    ask("Подходы"), ask("Повторения"), ask("Отдых, сек"))
                print("Упражнение добавлено в программу.")
            run_safely(add)
        elif choice == "2":
            def edit():
                item_id = ask_id("№ записи")
                if item_id is None:
                    return
                item = next((i for i in program_service.get_program_exercises(program_id)
                             if i.id == item_id), None)
                if not item:
                    print("В этой программе нет такой записи")
                    return
                program_service.update_program_exercise(
                    user, item_id, ask("Подходы", item.sets), ask("Повторения", item.reps),
                    ask("Отдых, сек", item.rest_seconds))
                print("Изменено.")
            run_safely(edit)
        elif choice == "3":
            def remove():
                item_id = ask_id("№ записи")
                if item_id is None:
                    return
                if not any(i.id == item_id for i in program_service.get_program_exercises(program_id)):
                    print("В этой программе нет такой записи")
                    return
                program_service.remove_exercise_from_program(user, item_id)
                print("Упражнение убрано из программы.")
            run_safely(remove)
        else:
            print("Нет такого пункта")


def programs_menu(user):
    while True:
        print("\n----- Тренировочные программы -----")
        print("1. Все программы")
        print("2. Мои программы")
        print("3. Программы по уровню сложности")
        print("4. Поиск по названию")
        print("5. Подробнее о программе")
        print("6. Создать программу")
        print("7. Изменить программу")
        print("8. Удалить программу")
        print("9. Состав программы (упражнения, подходы, отдых)")
        print("0. Назад")
        choice = input("Выберите действие: ").strip()
        actions = {
            "1": lambda: show_programs(program_service.get_all_programs()),
            "2": lambda: show_programs([p for p in program_service.get_all_programs()
                                        if p.trainer_id == user.user_id]),
            "3": programs_by_level_screen,
            "4": search_screen,
            "5": program_details_screen,
            "6": lambda: create_program_screen(user),
            "7": lambda: update_program_screen(user),
            "8": lambda: delete_program_screen(user),
            "9": lambda: program_content_menu(user),
        }
        if choice == "0":
            break
        if choice in actions:
            run_safely(actions[choice])
            if choice != "9":
                pause()
        else:
            print("Нет такого пункта")


# ---------- пользователи ----------

def users_menu(user):
    while True:
        print("\n----- Пользователи -----")
        print("1. Список пользователей")
        print("2. Добавить тренера")
        print("3. Удалить пользователя")
        print("0. Назад")
        choice = input("Выберите действие: ").strip()
        if choice == "0":
            break
        if choice == "1":
            print_table(["ID", "Логин", "ФИО", "Роль"],
                        [[u.user_id, u.login, u.full_name, u.role_name]
                         for u in user_service.get_all_users()])
        elif choice == "2":
            auth.add_trainer(user)
        elif choice == "3":
            def delete():
                user_id = ask_id("ID пользователя")
                if user_id is not None:
                    user_service.delete_user(user, user_id)
                    print("Пользователь удалён.")
            run_safely(delete)
        else:
            print("Нет такого пункта")
            continue
        pause()


def trainer_menu(user):
    while True:
        print(f"\n===== Тренер ({user.login}) =====")
        print("1. Тренировочные программы")
        print("2. Упражнения")
        print("3. Пользователи и тренеры")
        print("4. Сменить пароль")
        print("0. Выйти из аккаунта")
        choice = input("Выберите действие: ").strip()
        if choice == "1":
            programs_menu(user)
        elif choice == "2":
            exercises_menu()
        elif choice == "3":
            users_menu(user)
        elif choice == "4":
            auth.change_password(user)
        elif choice == "0":
            break
        else:
            print("Нет такого пункта")
