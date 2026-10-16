"""Відкриті тести задачі 4: Тип зв'язку й обов'язковість участі.

Запуск: pytest tests/test_variant_04.py
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
    ("S1", (model([], [rel("A", "zero_one", "B", "zero_one"), rel("B", "one_many", "C", "one"), rel("C", "one", "D", "one_many"), rel("D", "one_many", "E", "one_many")]),),
     [{'a': 'A', 'b': 'B', 'kind': '1:1', 'a_required': False, 'b_required': False},
      {'a': 'B', 'b': 'C', 'kind': 'N:1', 'a_required': True, 'b_required': True},
      {'a': 'C', 'b': 'D', 'kind': '1:N', 'a_required': True, 'b_required': True},
      {'a': 'D', 'b': 'E', 'kind': 'M:N', 'a_required': True, 'b_required': True}]),
    ("S2", (model([], [rel("CUSTOMER", "zero_one", "ORDERS", "zero_many", "робить")]),),
     [{'a': 'CUSTOMER', 'b': 'ORDERS', 'kind': '1:N', 'a_required': False, 'b_required': False}]),
    ("S3", (model([], [rel("TEACHER", "one", "STUDY_GROUP", "one", "куратор"), rel("TEACHER", "zero_many", "SUBJECT", "one_many", "викладає")]),),
     [{'a': 'TEACHER', 'b': 'STUDY_GROUP', 'kind': '1:1', 'a_required': True, 'b_required': True},
      {'a': 'TEACHER', 'b': 'SUBJECT', 'kind': 'M:N', 'a_required': True, 'b_required': False}]),
]


@pytest.mark.parametrize("case", CASES, ids=[f"{c[0]}-{i}" for i, c in enumerate(CASES)])
def test_classify_relationships(case):
    call = getattr(load(4), "classify_relationships")
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
