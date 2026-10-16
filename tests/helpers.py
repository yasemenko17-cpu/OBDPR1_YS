"""Допоміжні засоби тестів: компактне складання моделей і три предметні області.

Модель: {"entities": {ІМЯ: [атрибути]}, "relationships": [зв'язки]}.
Атрибут: {"type", "name", "keys"}. Зв'язок: {"a", "b", "a_card", "b_card", "identifying", "label"}.
Кардинальності: "one", "zero_one", "zero_many", "one_many".
"""
import copy


def attr(spec):
    """'int id PK' -> {"type": "int", "name": "id", "keys": ["PK"]}."""
    parts = spec.split()
    keys = [k for k in " ".join(parts[2:]).replace(",", " ").split()]
    return {"type": parts[0], "name": parts[1], "keys": keys}


def entity(name, *specs):
    return name, [attr(s) for s in specs]


def rel(a, a_card, b, b_card, label="", identifying=False):
    return {"a": a, "b": b, "a_card": a_card, "b_card": b_card, "identifying": identifying, "label": label}


def model(entities, rels):
    return {"entities": dict(entities), "relationships": list(rels)}


def clone(m):
    return copy.deepcopy(m)


def add_attr(m, entity_name, spec):
    m["entities"][entity_name].append(attr(spec))
    return m


def drop_attr(m, entity_name, attr_name):
    m["entities"][entity_name] = [a for a in m["entities"][entity_name] if a["name"] != attr_name]
    return m


def drop_rel(m, a, b):
    m["relationships"] = [r for r in m["relationships"] if {r["a"], r["b"]} != {a, b}]
    return m


# Набір 1: бібліотека
LIBRARY = model([
    entity("PUBLISHER", "int id PK", "string name"),
    entity("BOOK", "int id PK", "string title", "string isbn UK", "int publisher_id FK"),
    entity("AUTHOR", "int id PK", "string full_name"),
    entity("COPY", "int book_id PK,FK", "int copy_no PK", "string shelf"),
    entity("READER", "int id PK", "string full_name", "string email UK"),
    entity("LIBRARY_CARD", "int id PK", "date issued_on", "int reader_id FK,UK"),
    entity("LOAN", "int id PK", "date loaned_on", "int reader_id FK", "int book_id FK"),
], [
    rel("PUBLISHER", "one", "BOOK", "zero_many", "видає"),
    rel("BOOK", "zero_many", "AUTHOR", "one_many", "написана"),
    rel("BOOK", "one", "COPY", "one_many", "має примірники", True),
    rel("READER", "one", "LIBRARY_CARD", "zero_one", "отримує"),
    rel("READER", "one", "LOAN", "zero_many", "оформлює"),
    rel("BOOK", "one", "LOAN", "zero_many", "видається"),
])

# Набір 2: інтернет-магазин
SHOP = model([
    entity("CUSTOMER", "int id PK", "string name", "string email UK"),
    entity("ADDRESS", "int customer_id PK,FK", "int addr_no PK", "string city", "string street"),
    entity("CATEGORY", "int id PK", "string title"),
    entity("PRODUCT", "int id PK", "string title", "decimal price", "int category_id FK"),
    entity("TAG", "int id PK", "string name"),
    entity("ORDERS", "int id PK", "date created_on", "int customer_id FK"),
    entity("ORDER_LINE", "int orders_id PK,FK", "int line_no PK", "int qty", "int product_id FK"),
], [
    rel("CUSTOMER", "one", "ADDRESS", "zero_many", "має адреси", True),
    rel("CATEGORY", "one", "PRODUCT", "zero_many", "групує"),
    rel("PRODUCT", "zero_many", "TAG", "zero_many", "позначено"),
    rel("CUSTOMER", "one", "ORDERS", "zero_many", "робить"),
    rel("ORDERS", "one", "ORDER_LINE", "one_many", "містить", True),
    rel("PRODUCT", "one", "ORDER_LINE", "zero_many", "продається у"),
])

# Набір 3: навчальний заклад
COLLEGE = model([
    entity("TEACHER", "int id PK", "string full_name"),
    entity("STUDY_GROUP", "int id PK", "string code", "int teacher_id FK"),
    entity("STUDENT", "int id PK", "string full_name", "date birth_date", "int study_group_id FK"),
    entity("SUBJECT", "int id PK", "string title"),
    entity("LESSON", "int id PK", "date held_on", "int subject_id FK", "int teacher_id FK",
           "int study_group_id FK"),
    entity("ATTENDANCE", "int lesson_id PK,FK", "int student_id PK,FK", "bool present"),
], [
    rel("TEACHER", "zero_one", "STUDY_GROUP", "zero_many", "куратор"),
    rel("STUDY_GROUP", "one", "STUDENT", "one_many", "складається з"),
    rel("TEACHER", "zero_many", "SUBJECT", "zero_many", "викладає"),
    rel("SUBJECT", "one", "LESSON", "zero_many", "проводиться з"),
    rel("TEACHER", "one", "LESSON", "zero_many", "проводить"),
    rel("STUDY_GROUP", "one", "LESSON", "zero_many", "відвідує"),
    rel("LESSON", "one", "ATTENDANCE", "zero_many", "фіксує", True),
    rel("STUDENT", "one", "ATTENDANCE", "zero_many", "відмічається", True),
])


def set_keys(m, entity_name, attr_name, keys):
    for a in m["entities"][entity_name]:
        if a["name"] == attr_name:
            a["keys"] = list(keys)
    return m


def set_ident(m, a, b, value):
    for r in m["relationships"]:
        if {r["a"], r["b"]} == {a, b}:
            r["identifying"] = value
    return m


def set_card(m, a, b, side, value):
    for r in m["relationships"]:
        if {r["a"], r["b"]} == {a, b}:
            r[side] = value
    return m


def swap_rel(m, a, b):
    """Записує зв'язок у зворотному порядку (A↔B разом із кардинальностями)."""
    for r in m["relationships"]:
        if {r["a"], r["b"]} == {a, b}:
            r["a"], r["b"], r["a_card"], r["b_card"] = r["b"], r["a"], r["b_card"], r["a_card"]
    return m
