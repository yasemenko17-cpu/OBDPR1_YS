import copy

def lint_model(model):
    """
    Знаходить типові помилки ER-моделювання у моделі.
    Повертає відсортований список рядків у форматі 'КОД ОБ'ЄКТ'.
    """
    model_copy = copy.deepcopy(model)
    issues = set()
    entities = model_copy.get("entities", {})
    relationships = model_copy.get("relationships", [])
    
    entity_names = set(entities.keys())
    
    # Допоміжні функції для безпечного витягування даних зі зв'язку (словник чи кортеж)
    def get_rel_entities(rel):
        if isinstance(rel, dict):
            return rel.get("a"), rel.get("b")
        elif isinstance(rel, (list, tuple)) and len(rel) >= 2:
            return rel[0], rel[1]
        return None, None

    def get_rel_cards(rel):
        if isinstance(rel, dict):
            return rel.get("a_card") or rel.get("card_a"), rel.get("b_card") or rel.get("card_b")
        elif isinstance(rel, (list, tuple)) and len(rel) >= 4:
            return rel[2], rel[3]
        return None, None

    # 1. ISOLATED ІМЯ: сутність не бере участі в жодному зв'язку (якщо сутностей >= 2)
    if len(entities) >= 2:
        linked_entities = set()
        for rel in relationships:
            a, b = get_rel_entities(rel)
            if a: linked_entities.add(a)
            if b: linked_entities.add(b)
        
        for ent_name in entities:
            if ent_name not in linked_entities:
                issues.add(f"ISOLATED {ent_name}")

    for ent_name, attrs in entities.items():
        # 2. NO_ATTRS ІМЯ: у сутності немає атрибутів
        if not attrs:
            issues.add(f"NO_ATTRS {ent_name}")
            continue
            
        attr_names = []
        for attr in attrs:
            attr_name = attr.get("name")
            attr_type = attr.get("type")
            
            # 3. MULTIVALUED ІМЯ.атрибут: багатозначний атрибут (тип закінчується на [])
            if isinstance(attr_type, str) and attr_type.endswith("[]"):
                issues.add(f"MULTIVALUED {ent_name}.{attr_name}")
            
            # 4. ATTR_IS_ENTITY ІМЯ.атрибут: ім'я атрибута збігається з назвою іншої сутності
            if attr_name and attr_name.upper() in {e.upper() for e in entity_names if e != ent_name}:
                issues.add(f"ATTR_IS_ENTITY {ent_name}.{attr_name}")
                
            attr_names.append(attr_name)
            
        # 5. DUP_ATTR ІМЯ.атрибут: дублювання імені атрибута всередині сутності
        seen_attrs = set()
        for name in attr_names:
            if name in seen_attrs:
                issues.add(f"DUP_ATTR {ent_name}.{name}")
            seen_attrs.add(name)

    # 6. DUP_REL X Y: два й більше зв'язків між тією самою парою (імена впорядковані за абеткою)
    rel_pairs = {}
    for rel in relationships:
        a, b = get_rel_entities(rel)
        if a and b:
            pair = tuple(sorted([a, b]))
            rel_pairs[pair] = rel_pairs.get(pair, 0) + 1
        
    for (a, b), count in rel_pairs.items():
        if count > 1:
            issues.add(f"DUP_REL {a} {b}")

    # 7. MN_UNRESOLVED А В: нерозкладений зв'язок М:N
    many_types = {"zero_many", "one_many", "N", "n", "MANY", "many"}
    for rel in relationships:
        a, b = get_rel_entities(rel)
        card_a, card_b = get_rel_cards(rel)
        if a and b and card_a in many_types and card_b in many_types:
            issues.add(f"MN_UNRESOLVED {a} {b}")

    return sorted(list(issues))