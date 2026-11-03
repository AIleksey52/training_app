from dataclasses import dataclass


@dataclass
class Program:
    program_id: int
    name: str
    description: str | None
    duration_weeks: int
    level_id: int
    trainer_id: int
    level_name: str | None = None    # служебное поле: название уровня сложности
    trainer_name: str | None = None  # служебное поле: ФИО тренера
