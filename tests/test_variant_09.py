"""Відкриті тести задачі 9: Перевірка екземплярів даних.

Запуск: pytest tests/test_variant_09.py
Тут лише приклади з карток варіантів; повний набір перевірок є у викладача.
"""
import copy

import pytest
from conftest import load
from helpers import *  # noqa: F401,F403

LIB_DATA = {
    "PUBLISHER": [{"id": 1, "name": "Фоліо"}, {"id": 2, "name": "Ранок"}],
    "BOOK": [{"id": 10, "title": "Кобзар", "isbn": "A-1", "publisher_id": 1},
             {"id": 11, "title": "Лісова пісня", "isbn": "A-2", "publisher_id": 2}],
    "COPY": [{"book_id": 10, "copy_no": 1}, {"book_id": 10, "copy_no": 2}, {"book_id": 11, "copy_no": 1}],
    "READER": [{"id": 100, "full_name": "Ірина", "email": "i@x.ua"}, {"id": 101, "full_name": "Павло", "email": "p@x.ua"}],
    "LIBRARY_CARD": [{"id": 1, "reader_id": 100}],
    "LOAN": [{"id": 1, "reader_id": 100, "book_id": 10}, {"id": 2, "reader_id": 101, "book_id": 11}],
}
SHOP_DATA = {
    "CUSTOMER": [{"id": 1, "name": "Оксана"}, {"id": 2, "name": "Назар"}],
    "ADDRESS": [{"customer_id": 1, "addr_no": 1}, {"customer_id": 1, "addr_no": 2}],
    "CATEGORY": [{"id": 1, "title": "Книги"}],
    "PRODUCT": [{"id": 5, "category_id": 1}, {"id": 6, "category_id": 1}],
    "ORDERS": [{"id": 1, "customer_id": 2}, {"id": 2, "customer_id": 1}],
    "ORDER_LINE": [{"orders_id": 1, "line_no": 1, "product_id": 5}, {"orders_id": 1, "line_no": 2, "product_id": 6},
                   {"orders_id": 2, "line_no": 1, "product_id": 6}],
}
COLLEGE_DATA = {
    "TEACHER": [{"id": 1}, {"id": 2}],
    "STUDY_GROUP": [{"id": 1, "code": "A-11", "teacher_id": 1}, {"id": 2, "code": "B-21", "teacher_id": None}],
    "STUDENT": [{"id": 1, "study_group_id": 1}, {"id": 2, "study_group_id": 1}, {"id": 3, "study_group_id": 2}],
    "SUBJECT": [{"id": 1}],
    "LESSON": [{"id": 1, "subject_id": 1, "teacher_id": 2, "study_group_id": 1}],
    "ATTENDANCE": [{"lesson_id": 1, "student_id": 1, "present": True}, {"lesson_id": 1, "student_id": 2, "present": False}],
}


def patched(data, **changes):
    """Копія даних із заміною таблиць."""
    out = clone(data)
    out.update(changes)
    return out


def norm(value):
    """Кортежі й списки порівнюються однаково."""
    if isinstance(value, (list, tuple)):
        return [norm(v) for v in value]
    if isinstance(value, dict):
        return {k: norm(v) for k, v in value.items()}
    return value


CASES = [
    ("S1", (LIBRARY, patched(LIB_DATA, BOOK=[{"id": 10, "publisher_id": 1}, {"id": 11, "publisher_id": None}]),),
     ['NULL_FK BOOK[1].publisher_id']),
    ("S2", (SHOP, patched(SHOP_DATA, ORDERS=[{"id": 1, "customer_id": 2}, {"id": 2, "customer_id": None}, {"id": 3, "customer_id": 1}]),),
     ['NO_CHILD ORDERS[2]', 'NULL_FK ORDERS[1].customer_id']),
    ("S3", (COLLEGE, patched(COLLEGE_DATA, LESSON=[{"id": 1, "subject_id": 1, "teacher_id": None, "study_group_id": 1}]),),
     ['NULL_FK LESSON[0].teacher_id']),
]


@pytest.mark.parametrize("case", CASES, ids=[f"{c[0]}-{i}" for i, c in enumerate(CASES)])
def test_check_instances(case):
    call = getattr(load(9), "check_instances")
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
