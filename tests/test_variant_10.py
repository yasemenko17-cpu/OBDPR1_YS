"""Відкриті тести задачі 10: Порівняння моделей.

Запуск: pytest tests/test_variant_10.py
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
    ("S1", (LIBRARY, drop_rel(drop_attr(clone(LIBRARY), "READER", "email"), "READER", "LIBRARY_CARD"),),
     ['MISSING_ATTR READER.email', 'MISSING_REL LIBRARY_CARD READER']),
    ("S2", (SHOP, set_ident(set_keys(clone(SHOP), "PRODUCT", "category_id", []), "CATEGORY", "PRODUCT", True),),
     ['IDENT_MISMATCH CATEGORY PRODUCT', 'KEY_MISMATCH PRODUCT.category_id']),
    ("S3", (COLLEGE, set_card(set_card(clone(COLLEGE), "TEACHER", "STUDY_GROUP", "a_card", "one"), "TEACHER", "SUBJECT", "b_card", "zero_many"),),
     ['CARD_MISMATCH STUDY_GROUP TEACHER']),
]


@pytest.mark.parametrize("case", CASES, ids=[f"{c[0]}-{i}" for i, c in enumerate(CASES)])
def test_compare_models(case):
    call = getattr(load(10), "compare_models")
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
