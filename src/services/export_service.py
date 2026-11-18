"""ЛР5: выгрузка данных в форматы JSON, CSV, XML, YAML."""
from pathlib import Path

from repositories import program_exercise_repository, program_repository
from services import serializers

# корень проекта: src/services/export_service.py -> training_app/
OUT_DIR = Path(__file__).resolve().parents[2] / "out"


def get_programs_data() -> list[dict]:
    """Таблица programs + связанные данные (уровень, тренер, упражнения)
    в виде вложенной структуры."""
    exercises_by_program: dict[int, list[dict]] = {}
    for pe in program_exercise_repository.get_all():
        exercises_by_program.setdefault(pe.program_id, []).append({
            "position": pe.position,
            "exercise_id": pe.exercise_id,
            "name": pe.exercise_name,
            "sets": pe.sets,
            "reps": pe.reps,
            "rest_seconds": pe.rest_seconds,
        })

    data = []
    for p in program_repository.get_all():
        data.append({
            "program_id": p.program_id,
            "name": p.name,
            "description": p.description,
            "duration_weeks": p.duration_weeks,
            "level": {"level_id": p.level_id, "name": p.level_name},
            "trainer": {"user_id": p.trainer_id, "full_name": p.trainer_name},
            "exercises": exercises_by_program.get(p.program_id, []),
        })
    return data


def export_records(records: list[dict], out_dir: Path = OUT_DIR,
                   base_name: str = "data", root: str = "items",
                   item: str | None = None) -> list[Path]:
    """Универсальная выгрузка любого списка словарей в 4 формата.
    Создаёт папку out, если её нет. Возвращает пути созданных файлов."""
    out_dir.mkdir(parents=True, exist_ok=True)
    files = {
        "json": (serializers.to_json(records), "utf-8"),
        # utf-8-sig — чтобы Excel правильно показал кириллицу
        "csv": (serializers.to_csv(records), "utf-8-sig"),
        "xml": (serializers.to_xml(records, root=root, item=item), "utf-8"),
        "yaml": (serializers.to_yaml(records), "utf-8"),
    }
    paths = []
    for ext, (text, encoding) in files.items():
        path = out_dir / f"{base_name}.{ext}"
        with open(path, "w", encoding=encoding, newline="") as f:
            f.write(text)
        paths.append(path)
    return paths


def export_programs(out_dir: Path = OUT_DIR) -> list[Path]:
    return export_records(get_programs_data(), out_dir, root="programs", item="program")
