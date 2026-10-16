"""Відкриті тести задачі 5: Перевірка ключів.

Запуск: pytest tests/test_variant_05.py
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
    ("S1", (drop_attr(clone(LIBRARY), "LOAN", "book_id"),),
     ['MISSING_FK LOAN BOOK']),
    ("S2", (drop_attr(drop_attr(clone(SHOP), "ORDERS", "customer_id"), "PRODUCT", "category_id"),),
     ['MISSING_FK ORDERS CUSTOMER', 'MISSING_FK PRODUCT CATEGORY']),
    ("S3", (drop_attr(clone(COLLEGE), "STUDENT", "study_group_id"),),
     ['MISSING_FK STUDENT STUDY_GROUP']),
]


@pytest.mark.parametrize("case", CASES, ids=[f"{c[0]}-{i}" for i, c in enumerate(CASES)])
def test_validate_keys(case):
    call = getattr(load(5), "validate_keys")
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
