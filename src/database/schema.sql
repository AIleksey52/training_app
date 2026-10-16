DROP TABLE IF EXISTS program_exercises;
DROP TABLE IF EXISTS programs;
DROP TABLE IF EXISTS exercises;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS user_roles;
DROP TABLE IF EXISTS difficulty_levels;

CREATE TABLE difficulty_levels (
    level_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE user_roles (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    role_id INTEGER NOT NULL,
    FOREIGN KEY (role_id) REFERENCES user_roles (role_id)
);

CREATE TABLE exercises (
    exercise_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE programs (
    program_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    duration_weeks INTEGER NOT NULL CHECK (duration_weeks > 0),
    level_id INTEGER NOT NULL,
    trainer_id INTEGER NOT NULL,
    FOREIGN KEY (level_id) REFERENCES difficulty_levels (level_id),
    FOREIGN KEY (trainer_id) REFERENCES users (user_id)
);

CREATE TABLE program_exercises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_id INTEGER NOT NULL,
    exercise_id INTEGER NOT NULL,
    position INTEGER NOT NULL,
    sets INTEGER NOT NULL,
    reps INTEGER NOT NULL,
    rest_seconds INTEGER NOT NULL,
    FOREIGN KEY (program_id) REFERENCES programs (program_id) ON DELETE CASCADE,
    FOREIGN KEY (exercise_id) REFERENCES exercises (exercise_id),
    UNIQUE (program_id, position)
);

INSERT INTO difficulty_levels (name) VALUES ('Начальный'), ('Средний'), ('Продвинутый');
INSERT INTO user_roles (name) VALUES ('Тренер'), ('Спортсмен');

INSERT INTO users (login, full_name, role_id) VALUES
    ('trainer1', 'Иванов Пётр', 1),
    ('athlete1', 'Петров Сергей', 2),
    ('athlete2', 'Сидорова Анна', 2);

INSERT INTO exercises (name, description) VALUES
    ('Приседания', 'Базовое упражнение для ног'),
    ('Отжимания', 'Упражнение на грудь и трицепс'),
    ('Подтягивания', 'Упражнение на спину и бицепс'),
    ('Планка', 'Статическое упражнение на кор');

INSERT INTO programs (name, description, duration_weeks, level_id, trainer_id) VALUES
    ('Старт для новичков', 'Базовая программа на всё тело', 4, 1, 1),
    ('Сила и масса', 'Программа на набор силы', 8, 2, 1);

INSERT INTO program_exercises (program_id, exercise_id, position, sets, reps, rest_seconds) VALUES
    (1, 1, 1, 3, 12, 60),
    (1, 2, 2, 3, 10, 60),
    (1, 4, 3, 3, 30, 45),
    (2, 1, 1, 4, 8, 90),
    (2, 3, 2, 4, 6, 120);