"""Відкриті тести задачі 7: Розкладання зв'язку M:N.

Запуск: pytest tests/test_variant_07.py
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
    ("S1", (model([entity("A", "int id PK"), entity("B", "string code PK", "int n")], [rel("A", "one_many", "B", "one_many", "зв'язок")]),),
     {'entities': {'A': [{'type': 'int', 'name': 'id', 'keys': ['PK']}],
                   'B': [{'type': 'string', 'name': 'code', 'keys': ['PK']},
                         {'type': 'int', 'name': 'n', 'keys': []}],
                   'A_B': [{'type': 'int', 'name': 'a_id', 'keys': ['PK', 'FK']},
                           {'type': 'string', 'name': 'b_code', 'keys': ['PK', 'FK']}]},
      'relationships': [{'a': 'A',
                         'b': 'A_B',
                         'a_card': 'one',
                         'b_card': 'one_many',
                         'identifying': True,
                         'label': "зв'язок"},
                        {'a': 'B',
                         'b': 'A_B',
                         'a_card': 'one',
                         'b_card': 'one_many',
                         'identifying': True,
                         'label': "зв'язок"}]}),
    ("S2", (model([entity("STUDENT", "int id PK"), entity("COURSE", "int year PK", "int no PK")], [rel("STUDENT", "zero_many", "COURSE", "zero_many", "записаний")]),),
     {'entities': {'STUDENT': [{'type': 'int', 'name': 'id', 'keys': ['PK']}],
                   'COURSE': [{'type': 'int', 'name': 'year', 'keys': ['PK']},
                              {'type': 'int', 'name': 'no', 'keys': ['PK']}],
                   'STUDENT_COURSE': [{'type': 'int', 'name': 'student_id', 'keys': ['PK', 'FK']},
                                      {'type': 'int', 'name': 'course_year', 'keys': ['PK', 'FK']},
                                      {'type': 'int', 'name': 'course_no', 'keys': ['PK', 'FK']}]},
      'relationships': [{'a': 'STUDENT',
                         'b': 'STUDENT_COURSE',
                         'a_card': 'one',
                         'b_card': 'zero_many',
                         'identifying': True,
                         'label': 'записаний'},
                        {'a': 'COURSE',
                         'b': 'STUDENT_COURSE',
                         'a_card': 'one',
                         'b_card': 'zero_many',
                         'identifying': True,
                         'label': 'записаний'}]}),
    ("S3", (model([entity("A", "int id PK"), entity("B", "int id PK"), entity("A_B", "int x PK")], [rel("A", "zero_many", "B", "zero_many", "x")]),),
     ValueError('Сутність A_B вже існує')),
]


@pytest.mark.parametrize("case", CASES, ids=[f"{c[0]}-{i}" for i, c in enumerate(CASES)])
def test_resolve_many_to_many(case):
    call = getattr(load(7), "resolve_many_to_many")
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
