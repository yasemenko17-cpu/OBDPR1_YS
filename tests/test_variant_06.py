"""Відкриті тести задачі 6: Слабкі сутності.

Запуск: pytest tests/test_variant_06.py
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
    ("S1", (set_keys(clone(LIBRARY), "COPY", "book_id", ["FK"]),),
     {'COPY': {'owners': ['BOOK'], 'key_ok': False, 'total': True}}),
    ("S2", (set_card(clone(SHOP), "ORDERS", "ORDER_LINE", "a_card", "zero_one"),),
     {'ADDRESS': {'owners': ['CUSTOMER'], 'key_ok': True, 'total': True},
      'ORDER_LINE': {'owners': ['ORDERS'], 'key_ok': True, 'total': False}}),
    ("S3", (set_keys(clone(COLLEGE), "ATTENDANCE", "student_id", ["PK"]),),
     {'ATTENDANCE': {'owners': ['LESSON', 'STUDENT'], 'key_ok': False, 'total': True}}),
]


@pytest.mark.parametrize("case", CASES, ids=[f"{c[0]}-{i}" for i, c in enumerate(CASES)])
def test_weak_entities(case):
    call = getattr(load(6), "weak_entities")
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
