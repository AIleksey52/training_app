"""Универсальные сериализаторы: принимают список словарей любой структуры
(с вложенными словарями и списками) и превращают его в JSON, CSV, XML, YAML.
От конкретной таблицы не зависят."""
import csv
import io
import json
from xml.dom import minidom
from xml.etree import ElementTree as ET


# ---------- JSON ----------

def to_json(records: list[dict]) -> str:
    return json.dumps(records, ensure_ascii=False, indent=2)


# ---------- CSV ----------

def _flatten(record: dict, prefix: str = "") -> dict:
    """Вложенный словарь -> плоский: {"level": {"name": "x"}} -> {"level.name": "x"}.
    Список объединяется в одну ячейку (CSV не поддерживает вложенность)."""
    flat = {}
    for key, value in record.items():
        name = f"{prefix}{key}"
        if isinstance(value, dict):
            flat.update(_flatten(value, name + "."))
        elif isinstance(value, list):
            parts = []
            for item in value:
                if isinstance(item, dict):
                    parts.append(", ".join(f"{k}={v}" for k, v in _flatten(item).items()))
                else:
                    parts.append(str(item))
            flat[name] = " | ".join(parts)
        else:
            flat[name] = "" if value is None else value
    return flat


def to_csv(records: list[dict], delimiter: str = ";") -> str:
    rows = [_flatten(r) for r in records]
    headers = []
    for row in rows:                       # собираем все колонки, сохраняя порядок
        for key in row:
            if key not in headers:
                headers.append(key)
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=headers, delimiter=delimiter,
                            lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


# ---------- XML ----------

def _singular(name: str) -> str:
    """Имя элемента списка: exercises -> exercise, иначе item."""
    return name[:-1] if name.endswith("s") and len(name) > 1 else "item"


def _fill_xml(parent: ET.Element, value):
    if isinstance(value, dict):
        for key, child_value in value.items():
            _fill_xml(ET.SubElement(parent, key), child_value)
    elif isinstance(value, list):
        for item in value:
            _fill_xml(ET.SubElement(parent, _singular(parent.tag)), item)
    elif value is None:
        parent.set("null", "true")
    elif isinstance(value, bool):
        parent.text = "true" if value else "false"
    else:
        parent.text = str(value)


def to_xml(records: list[dict], root: str = "items", item: str | None = None) -> str:
    root_el = ET.Element(root)
    for record in records:
        _fill_xml(ET.SubElement(root_el, item or _singular(root)), record)
    raw = ET.tostring(root_el, encoding="unicode")
    return minidom.parseString(raw).toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")


# ---------- YAML ----------

def _yaml_scalar(value) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    # строка в двойных кавычках — корректна для YAML и экранирует спецсимволы
    return json.dumps(str(value), ensure_ascii=False)


def _yaml_lines(value, indent: int) -> list[str]:
    pad = " " * indent
    lines = []
    if isinstance(value, dict):
        for key, child in value.items():
            if isinstance(child, (dict, list)) and child:
                lines.append(f"{pad}{key}:")
                lines.extend(_yaml_lines(child, indent + 2))
            elif isinstance(child, (dict, list)):
                lines.append(f"{pad}{key}: {'{}' if isinstance(child, dict) else '[]'}")
            else:
                lines.append(f"{pad}{key}: {_yaml_scalar(child)}")
    elif isinstance(value, list):
        for item in value:
            if isinstance(item, (dict, list)) and item:
                item_lines = _yaml_lines(item, indent + 2)
                item_lines[0] = f"{pad}- " + item_lines[0].lstrip()
                lines.extend(item_lines)
            else:
                lines.append(f"{pad}- {_yaml_scalar(item)}")
    return lines


def to_yaml(records: list[dict]) -> str:
    return "\n".join(_yaml_lines(records, 0)) + "\n"
