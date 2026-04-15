# Open Data AI Analytics

# Мета
Аналіз відкритих даних та побудова моделей

## Джерело даних
https://data.gov.ua/dataset/6da6e500-e3c0-4a6a-9cb1-764582b531ee/resource/4de9eaa3-bf2b-48cc-bae7-ba4866187a6f

## Питання / гіпотези
1. Яка організація укладає найдорожчі контракти і чому?
2. Чи впливає кількість підрозділів на загальну вартість контракту?
3. Які регіони отримують найбільше контрактів?
Another conflicting line from main
Conflict test from feature/conflict_test

###  Хід роботи

#### 1 Ініціалізація репозиторію
- Створено репозиторій `open-data-ai-analytics`.
- Додано структуру та файли (`README.md`, `.gitignore`, `data/README.md`).
- Налаштовано `.gitignore` для:
  - `__pycache__/`, `.ipynb_checkpoints/`
  - `.venv/`, `.env`
  - `data/raw/` 
- Коміт: `Initial project structure`

#### 2 Завантаження даних
- Створена гілка `feature/data_load`
- Доданий скрипт `src/data_load.py` для завантаження CSV датасету
- Після перевірки та тестування змінено main через merge:
  - Коміт: `Add data loading script`
  - Merge завершено у main

#### 3 Перевірка якості даних
- Створена гілка `feature/data_quality_analysis`
- Доданий скрипт `src/data_quality_analysis.py`:
  - Перевірка пропусків, дублікатів, типів даних
- Merge у main через PR:
  - Коміт: `Add data quality analysis`

#### 4 Аналіз даних та побудова моделей
- Створена гілка `feature/data_research`
- Доданий скрипт `src/data_research.py`:
  - Попередній аналіз даних
  - Визначення закономірностей і перевірка гіпотез
- Merge у main через PR:
  - Коміт: `Add initial data exploration`

#### 5 Merge-конфлікт
- Створена гілка `feature/conflict_test`
- Додано зміну у README, яка конфліктує з іншою гілкою
- Merge у main призвів до конфлікту
- Конфлікт вирішено вручну у файлі `README.md`
- Коміт: `Resolve merge conflict in README`

#### 6 Візуалізація
- Створена гілка `feature/visualization`
- Доданий скрипт `src/visualization.py`
- Merge у main:
  - Коміт: `Add basic data visualization script`

#### 7 CHANGELOG і тег релізу
- Додано `CHANGELOG.md` для відстеження змін
- Створено тег `v0.1.0` для поточної версії

###  Гілки репозиторію
На GitHub створено гілки:

- `main`
- `feature/data_load`
- `feature/data_quality_analysis`
- `feature/data_research`
- `feature/visualization`
- `feature/conflict_test`

###  Git log
```text
* 5f2b64b (HEAD -> main, origin/main) Ignore nested repository folder
* 0e7d308 Ignore nested repository folder
* 200303c Ignore nested repository folder
* 94ff026 Remove nested repository and stage real project files
* 51e118d (tag: v0.1.0) Add CHANGELOG
* fd9d4e7 (origin/feature/visualization, feature/visualization) Add basic data visualization script
*   d70f429 Resolve merge conflict in README
|\
| * c46daa6 (origin/feature/conflict_test, feature/conflict_test) Add conflicting line to README
* | b5f39e9 Add another conflicting line to README 


# Dockerized Data Analysis Project

## Опис проєкту

Проєкт складається з кількох контейнеризованих сервісів:
- `data_load` — зчитує CSV-файл, створює SQLite-базу та завантажує дані;
- `data_quality_analysis` — виконує перевірку якості даних та формує звіт;
- `data_research` — обчислює базові статистики та формує підсумковий звіт;
- `visualization` — будує графіки та зберігає їх у `PNG`;
- `web` — показує звіти та візуалізації у браузері.

## Структура проєкту

```text
project/
├── data/
│   └── dataset.csv
├── data_load/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── data_quality_analysis/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── data_research/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── visualization/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── web/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── templates/
│   │   └── index.html
│   └── static/
│       └── style.css
├── reports/
├── plots/
├── storage/
├── compose.yaml
└── README.md
```

## Використані технології

- Python 3.12
- Pandas
- SQLite
- Matplotlib
- Seaborn
- Flask
- Docker
- Docker Compose

## Як запустити

1. Переконайтесь, що встановлено Docker і Docker Compose.
2. Перейдіть у корінь проєкту.
3. Запустіть:

```bash
docker compose up --build
```

4. Відкрийте браузер і перейдіть за адресою:

```text
http://localhost:5000
```

## Опис сервісів

### `data_load`
- читає `data/dataset.csv`;
- створює таблицю `contracts` у SQLite;
- записує базу у volume `storage`.

### `data_quality_analysis`
- читає дані з бази;
- рахує пропуски;
- перевіряє дублікати;
- перевіряє коректність дат і числових значень;
- зберігає звіт у `reports/`.

### `data_research`
- обчислює описову статистику;
- формує текстовий та JSON-звіт;
- зберігає результат у `reports/`.

### `visualization`
- будує 2 графіки;
- зберігає їх у `plots/`.

### `web`
- запускає Flask-інтерфейс;
- відображає звіти;
- показує графіки у браузері.

## Порти

- `web`: `5000:5000`

## Взаємодія між сервісами

- `data_load` створює SQLite-базу у спільному volume `storage`;
- `data_quality_analysis`, `data_research` і `visualization` читають дані з цієї БД;
- результати записуються у volumes `reports` і `plots`;
- `web` читає ці результати та показує їх користувачу.

## Приклад CSV

Файл `data/dataset.csv` повинен містити колонки:

```text
legal_entity_id,legal_entity_edrpou,legal_entity_name,contract_number,contract_date,contract_start_date,contract_end_date,last_update_contract,package_id,package_contract_price,all_contract_price,contract_count_division_id,contract_divisions
```

## Корисні команди

Зупинити сервіси:

```bash
docker compose down
```

Перебудувати образи:

```bash
docker compose up --build
```

Подивитись запущені контейнери:

```bash
docker ps
```