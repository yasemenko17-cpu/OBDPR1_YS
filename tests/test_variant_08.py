"""Відкриті тести задачі 8: Типові помилки ER-моделювання.

Запуск: pytest tests/test_variant_08.py
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
    ("S1", (model([entity("A", "int id PK"), entity("B", "int id PK"), entity("C", "int id PK")], [rel("A", "one", "B", "zero_many")]),),
     ['ISOLATED C']),
    ("S2", (add_attr(clone(SHOP), "PRODUCT", "string category"),),
     ['ATTR_IS_ENTITY PRODUCT.category', 'MN_UNRESOLVED PRODUCT TAG']),
    ("S3", (model([entity("ROOM"), entity("DESK", "int id PK", "int room")], [rel("ROOM", "one", "DESK", "zero_many", "містить")]),),
     ['ATTR_IS_ENTITY DESK.room', 'NO_ATTRS ROOM']),
]


@pytest.mark.parametrize("case", CASES, ids=[f"{c[0]}-{i}" for i, c in enumerate(CASES)])
def test_lint_model(case):
    call = getattr(load(8), "lint_model")
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
