# Стартовий проєкт OBDZ-P01

1. Відкрийте проєкт у GitHub Codespaces (Code → Codespaces → Create codespace) або локально: `python3 -m venv .venv`, `source .venv/bin/activate` (у Windows: `.venv\Scripts\activate`), `pip install -r requirements.txt`.
2. Визначте свою задачу за номером варіанта: задача = `(номер - 1) // 3 + 1`, набір = `(номер - 1) % 3 + 1`. Реалізуйте задачу у файлі `variants/variant_NN.py` за карткою.
3. Запускайте відкриті тести своєї задачі: `pytest tests/test_variant_NN.py` (NN з двома цифрами). Права адміністратора не потрібні, PostgreSQL не потрібен.
4. Змінюйте лише свій файл у `variants/`, файл `tests/test_my.py` і свою діаграму `my_model/model.mmd`.
5. Моделі трьох наборів лежать у `data/` (`library.mmd`, `shop.mmd`, `college.mmd`), описи предметних областей для власної діаграми у `data/own_domain_N.md`. Перевірка власної діаграми: `python check_my_model.py my_model/model.mmd`. Частина Б (діаграма за темою власного диплома): ваш опис у `my_model/diploma_domain.md`, діаграма в `my_model/diploma.mmd`, перевірка тією ж командою: `python check_my_model.py my_model/diploma.mmd`.
