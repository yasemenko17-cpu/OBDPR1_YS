"""Відкриті тести задачі 2: Запис моделі у текст Mermaid.

Запуск: pytest tests/test_variant_02.py
Тут лише приклади з карток варіантів; повний набір перевірок є у викладача.
"""
import copy

import pytest
from conftest import load
from helpers import *  # noqa: F401,F403


def norm(value):
    """Кортежі й списки порівнюються однаково."""
    if isinstance(value, (list, tuple)):
        return [norm(v) for v in value]
    if isinstance(value, dict):
        return {k: norm(v) for k, v in value.items()}
    return value


CASES = [
    ("S1", (model([entity("PUBLISHER", "int id PK", "string name"), entity("BOOK", "int id PK", "int publisher_id FK")], [rel("PUBLISHER", "one", "BOOK", "zero_many", "видає")]),),
     ('erDiagram\n'
      '    PUBLISHER {\n'
      '        int id PK\n'
      '        string name\n'
      '    }\n'
      '    BOOK {\n'
      '        int id PK\n'
      '        int publisher_id FK\n'
      '    }\n'
      '\n'
      '    PUBLISHER ||..o{ BOOK : "видає"\n')),
    ("S2", (model([entity("A"), entity("B", "int id PK, FK, UK", "string note")], [rel("A", "zero_one", "B", "one_many", "зв'язок", True)]),),
     ('erDiagram\n'
      '    A {\n'
      '    }\n'
      '    B {\n'
      '        int id PK, FK, UK\n'
      '        string note\n'
      '    }\n'
      '\n'
      '    A |o--|{ B : "зв\'язок"\n')),
    ("S3", (model([entity("X", "int id UK, PK")], [rel("X", "zero_many", "X", "zero_many", "дружить")]),),
     'erDiagram\n    X {\n        int id UK, PK\n    }\n\n    X }o..o{ X : "дружить"\n'),
]


@pytest.mark.parametrize("case", CASES, ids=[f"{c[0]}-{i}" for i, c in enumerate(CASES)])
def test_render_er(case):
    call = getattr(load(2), "render_er")
    args = case[1]
    expected = case[2]
    before = copy.deepcopy(args)
    if isinstance(expected, ValueError):
        with pytest.raises(ValueError) as info:
            call(*args)
        assert str(info.value) == str(expected)
    else:
        assert norm(call(*args)) == norm(expected)
    assert args == before, "функція не повинна змінювати вхідні дані"
