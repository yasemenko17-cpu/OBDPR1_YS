"""Відкриті тести задачі 1: Розбір тексту Mermaid у модель.

Запуск: pytest tests/test_variant_01.py
Тут лише приклади з карток варіантів; повний набір перевірок є у викладача.
"""
import copy

import pytest
from conftest import load
from helpers import *  # noqa: F401,F403

TXT_SMALL = """erDiagram
    %% навчальний приклад
    PUBLISHER {
        int id PK
        string name
    }
    BOOK {
        int id PK
        string title
        int publisher_id FK
    }

    PUBLISHER ||..o{ BOOK : "видає"
"""
TXT_ONLY_RELS = """erDiagram
    A ||--|| B : "x"
    B }o..o{ C : "y"
    C |o--|{ A : z
"""
TXT_KEYS = "erDiagram\r\n\tITEM {\r\n\t\tint id FK PK\r\n\t\tstring code UK\r\n\t\tint owner_id PK,FK , UK\r\n\t\tstring note\r\n\t}\r\n"
TXT_NOHEAD = "graph TD\n    A --> B\n"
TXT_EMPTY = "  \n"
TXT_BADKEY = """erDiagram
    BOOK {
        int id PK
        string isbn XK
    }
"""
TXT_UNCLOSED = """erDiagram
    TEACHER {
        int id PK
        string full_name
"""
TXT_BADREL = """erDiagram
    TEACHER {
        int id PK
    }
    TEACHER ||==o{ LESSON : "проводить"
"""
TXT_DUP = """erDiagram
    TAG {
        int id PK
    }
    TAG {
        string name
    }
"""
TXT_ONEWORD = """erDiagram
    TAG {
        int id PK
        name
    }
"""
TXT_LIBRARY = """erDiagram
    PUBLISHER {
        int id PK
        string name
    }
    BOOK {
        int id PK
        string title
        string isbn UK
        int publisher_id FK
    }
    AUTHOR {
        int id PK
        string full_name
    }
    COPY {
        int book_id PK, FK
        int copy_no PK
        string shelf
    }
    READER {
        int id PK
        string full_name
        string email UK
    }
    LIBRARY_CARD {
        int id PK
        date issued_on
        int reader_id FK, UK
    }
    LOAN {
        int id PK
        date loaned_on
        int reader_id FK
        int book_id FK
    }

    PUBLISHER ||..o{ BOOK : "видає"
    BOOK }o..|{ AUTHOR : "написана"
    BOOK ||--|{ COPY : "має примірники"
    READER ||..o| LIBRARY_CARD : "отримує"
    READER ||..o{ LOAN : "оформлює"
    BOOK ||..o{ LOAN : "видається"
"""
TXT_SHOP = """erDiagram
    CUSTOMER {
        int id PK
        string name
        string email UK
    }
    ADDRESS {
        int customer_id PK, FK
        int addr_no PK
        string city
        string street
    }
    CATEGORY {
        int id PK
        string title
    }
    PRODUCT {
        int id PK
        string title
        decimal price
        int category_id FK
    }
    TAG {
        int id PK
        string name
    }
    ORDERS {
        int id PK
        date created_on
        int customer_id FK
    }
    ORDER_LINE {
        int orders_id PK, FK
        int line_no PK
        int qty
        int product_id FK
    }

    CUSTOMER ||--o{ ADDRESS : "має адреси"
    CATEGORY ||..o{ PRODUCT : "групує"
    PRODUCT }o..o{ TAG : "позначено"
    CUSTOMER ||..o{ ORDERS : "робить"
    ORDERS ||--|{ ORDER_LINE : "містить"
    PRODUCT ||..o{ ORDER_LINE : "продається у"
"""
TXT_COLLEGE = """erDiagram
    TEACHER {
        int id PK
        string full_name
    }
    STUDY_GROUP {
        int id PK
        string code
        int teacher_id FK
    }
    STUDENT {
        int id PK
        string full_name
        date birth_date
        int study_group_id FK
    }
    SUBJECT {
        int id PK
        string title
    }
    LESSON {
        int id PK
        date held_on
        int subject_id FK
        int teacher_id FK
        int study_group_id FK
    }
    ATTENDANCE {
        int lesson_id PK, FK
        int student_id PK, FK
        bool present
    }

    TEACHER |o..o{ STUDY_GROUP : "куратор"
    STUDY_GROUP ||..|{ STUDENT : "складається з"
    TEACHER }o..o{ SUBJECT : "викладає"
    SUBJECT ||..o{ LESSON : "проводиться з"
    TEACHER ||..o{ LESSON : "проводить"
    STUDY_GROUP ||..o{ LESSON : "відвідує"
    LESSON ||--o{ ATTENDANCE : "фіксує"
    STUDENT ||--o{ ATTENDANCE : "відмічається"
"""


def norm(value):
    """Кортежі й списки порівнюються однаково."""
    if isinstance(value, (list, tuple)):
        return [norm(v) for v in value]
    if isinstance(value, dict):
        return {k: norm(v) for k, v in value.items()}
    return value


CASES = [
    ("S1", (TXT_SMALL,),
     {'entities': {'PUBLISHER': [{'type': 'int', 'name': 'id', 'keys': ['PK']},
                                 {'type': 'string', 'name': 'name', 'keys': []}],
                   'BOOK': [{'type': 'int', 'name': 'id', 'keys': ['PK']},
                            {'type': 'string', 'name': 'title', 'keys': []},
                            {'type': 'int', 'name': 'publisher_id', 'keys': ['FK']}]},
      'relationships': [{'a': 'PUBLISHER',
                         'b': 'BOOK',
                         'a_card': 'one',
                         'b_card': 'zero_many',
                         'identifying': False,
                         'label': 'видає'}]}),
    ("S2", (TXT_SHOP,),
     SHOP),
    ("S3", (TXT_COLLEGE,),
     COLLEGE),
    ("S2", (TXT_NOHEAD,),
     ValueError('Очікується рядок erDiagram')),
    ("S3", (TXT_UNCLOSED,),
     ValueError('Не закрито блок сутності TEACHER')),
]


@pytest.mark.parametrize("case", CASES, ids=[f"{c[0]}-{i}" for i, c in enumerate(CASES)])
def test_parse_er(case):
    call = getattr(load(1), "parse_er")
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
