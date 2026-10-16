"""Швидка перевірка власної ER-моделі студента (текст Mermaid erDiagram).

Використання:  python check_my_model.py my_model/model.mmd
Скрипт самостійний і не залежить від ваших розв'язків задач: він лише повідомляє, які вимоги до моделі не виконано.
"""
import re
import sys

NAME = r"[A-Za-z_][A-Za-z0-9_]*"
HEAD = re.compile(rf"^({NAME})\s*\{{$")
REL = re.compile(rf"^({NAME})\s+(\|\||\|o|\}}o|\}}\|)(--|\.\.)(\|\||o\||o\{{|\|\{{)\s+({NAME})\s*:\s*(.+)$")


def check(text: str) -> list:
    """Повертає список зауважень до моделі (порожній список означає, що вимоги виконано)."""
    problems = []
    lines = [l.strip() for l in text.splitlines() if l.strip() and not l.strip().startswith("%%")]
    if not lines or lines[0] != "erDiagram":
        return ["Перший рядок файла має бути erDiagram"]
    entities, rels, current = {}, [], None
    for line in lines[1:]:
        if current is not None:
            if line == "}":
                current = None
            else:
                parts = line.split()
                if len(parts) < 2:
                    problems.append(f"Незрозумілий атрибут у сутності {current}: {line}")
                else:
                    keys = set(" ".join(parts[2:]).replace(",", " ").split())
                    entities[current].append((parts[1], keys))
            continue
        m = HEAD.match(line)
        if m:
            current = m.group(1)
            entities[current] = []
            continue
        m = REL.match(line)
        if m:
            rels.append(m.groups())
            for name in (m.group(1), m.group(5)):
                entities.setdefault(name, [])
            continue
        problems.append(f"Незрозумілий рядок: {line}")
    if current is not None:
        problems.append(f"Не закрито блок сутності {current}")
    if len(entities) < 6:
        problems.append(f"Сутностей {len(entities)}, потрібно щонайменше 6")
    if len(rels) < 5:
        problems.append(f"Зв'язків {len(rels)}, потрібно щонайменше 5")
    pk = {n: [a for a, k in attrs if "PK" in k] for n, attrs in entities.items()}
    for name, keys in pk.items():
        if not keys:
            problems.append(f"Сутність {name} не має первинного ключа")
    for name, attrs in entities.items():
        for attr, keys in attrs:
            if "FK" in keys and not any(attr == f"{o.lower()}_{p}" for o, ps in pk.items() if o != name for p in ps):
                problems.append(f"Зовнішній ключ {name}.{attr} не вказує на сутність за угодою <сутність_малими>_<ключ>")
    linked = {n for r in rels for n in (r[0], r[4])}
    for name in entities:
        if name not in linked:
            problems.append(f"Сутність {name} не має жодного зв'язку")
    for a, lc, dash, rc, b, label in rels:
        a_many, b_many = lc in ("}o", "}|"), rc in ("o{", "|{")
        if a_many and b_many:
            problems.append(f"Зв'язок M:N між {a} і {b} треба розкласти на асоціативну сутність")
        elif a_many != b_many:
            parent, child = (a, b) if b_many else (b, a)
            if not any("FK" in k and attr.startswith(parent.lower() + "_") for attr, k in entities.get(child, [])):
                problems.append(f"Сутність {child} не має зовнішнього ключа на {parent}")
    if not any(r[2] == "--" for r in rels):
        problems.append("Немає жодного ідентифікуючого зв'язку (--) для слабкої сутності")
    if not any(r[1] == "|o" or r[3] == "o|" for r in rels):
        problems.append("Немає жодного зв'язку з необов'язковою участю одного боку (|o або o|)")
    return problems


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    with open(argv[1], encoding="utf-8") as handle:
        problems = check(handle.read())
    for p in problems:
        print("-", p)
    print("Модель відповідає вимогам." if not problems else f"Зауважень: {len(problems)}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
