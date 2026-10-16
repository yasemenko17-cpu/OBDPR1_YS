import pytest
from variants.variant_08 import lint_model
from tests.helpers import model, entity

def test_my_lint_model_isolated():
    # Тест на виявлення ізольованих сутностей
    m = model([entity("A", "int id PK"), entity("B", "int id PK")], [])
    res = lint_model(m)
    assert any("ISOLATED" in str(err) for err in res)

def test_my_lint_model_valid():
    # Тест для валідної моделі без зауважень
    m = model(
        [
            entity("USER", "int id PK", "string name"),
            entity("COURSE", "int id PK", "int user_id FK", "string title")
        ],
        [
            ("USER", "COURSE", "1", "N", "створює", True)
        ]
    )
    res = lint_model(m)
    assert len(res) == 0