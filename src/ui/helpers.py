def ask(prompt: str, default: str | None = None) -> str:
    """Ввод строки. Если задан default — пустой ввод оставляет текущее значение."""
    hint = f" [{default}]" if default not in (None, "") else ""
    value = input(f"{prompt}{hint}: ").strip()
    if not value and default is not None:
        return str(default)
    return value


def ask_id(prompt: str) -> int | None:
    value = input(f"{prompt}: ").strip()
    if not value.isdigit():
        print("Нужно ввести номер (целое число).")
        return None
    return int(value)


def print_table(headers: list[str], rows: list[list]):
    if not rows:
        print("  (пусто)")
        return
    rows = [["" if c is None else str(c) for c in r] for r in rows]
    widths = [max(len(h), *(len(r[i]) for r in rows)) for i, h in enumerate(headers)]
    line = "  ".join(h.ljust(w) for h, w in zip(headers, widths))
    print(line)
    print("-" * len(line))
    for r in rows:
        print("  ".join(c.ljust(w) for c, w in zip(r, widths)))


def pause():
    input("\nНажмите Enter, чтобы продолжить...")
