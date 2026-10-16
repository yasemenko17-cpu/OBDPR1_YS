"""Відкриті тести задачі 3: Зв'язок із бізнес-правил.

Запуск: pytest tests/test_variant_03.py
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
    ("S1", ("PUBLISHER → BOOK: довільна кількість", "BOOK → PUBLISHER: рівно один", "видає",),
     {'a': 'PUBLISHER',
      'b': 'BOOK',
      'a_card': 'one',
      'b_card': 'zero_many',
      'identifying': False,
      'label': 'видає'}),
    ("S2", ("ORDERS → ORDER_LINE: принаймні один", "ORDER_LINE → ORDERS: рівно один", "містить", True,),
     {'a': 'ORDERS',
      'b': 'ORDER_LINE',
      'a_card': 'one',
      'b_card': 'one_many',
      'identifying': True,
      'label': 'містить'}),
    ("S3", ("TEACHER → STUDY_GROUP: довільна кількість", "STUDY_GROUP → TEACHER: не більше одного", "куратор",),
     {'a': 'TEACHER',
      'b': 'STUDY_GROUP',
      'a_card': 'zero_one',
      'b_card': 'zero_many',
      'identifying': False,
      'label': 'куратор'}),
    ("S3", ("STUDENT → LESSON: довільна кількість", "LESSON → TEACHER: рівно один",),
     ValueError('Правила описують різні пари сутностей')),
    ("S3", ("STUDENT → LESSON: багато", "LESSON → STUDENT: рівно один",),
     ValueError('Невідома кількість: багато')),
]


@pytest.mark.parametrize("case", CASES, ids=[f"{c[0]}-{i}" for i, c in enumerate(CASES)])
def test_relationship_from_rules(case):
    call = getattr(load(3), "relationship_from_rules")
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
