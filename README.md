# Open Data AI Analytics
# Лабораторна 1
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
```text

## Лабораторна 2

### Мета
Налаштувати CI/CD для проекту: автоматичний запуск модульних задач (тести, лінт, збірка, перевірки) при push або pull_request, публікація артефактів (логи, звіти, графіки) та навчитися запускати pipeline на GitHub-hosted та self-hosted runners.

### Хід роботи

#### 1. Створення workflow
Створено файл `.github/workflows/ci.yml` для налаштування CI/CD pipeline.

#### 2. Визначення тригерів
- `push` у гілку main (автоматичний запуск після коміту)  
- `pull_request` у гілку main (при створенні PR)  
- `workflow_dispatch` (ручний запуск з вибором модуля)

#### 3. Налаштування job run-modules
Job `run-modules` виконується на Ubuntu (`runs-on: ubuntu-latest`) і використовує matrix для одночасного запуску всіх модулів: `data_load`, `data_quality`, `data_research`, `visualization`. Параметр `fail-fast: false` забезпечує продовження запуску інших модулів навіть при падінні одного.

Job виконує:
- checkout коду з репозиторію  
- встановлення Python 3.11 та залежностей з `requirements.txt`  
- запуск модулів: якщо обрано всі модулі (`all`), workflow проходить циклічний запуск по кожному модулю і результати записуються у `artifacts/<module>/log.txt`; якщо обрано конкретний модуль — запускається тільки він  
- збереження результатів через `actions/upload-artifact@v4` для подальшого аналізу логів та артефактів

Matrix стратегія дозволяє паралельно запускати модулі без дублювання коду, а параметр `module` у `workflow_dispatch` економить час.

#### 4. Публікація результатів
Реалізовано варіант 1: після запуску модулів всі результати зберігаються як GitHub Actions artifacts. Це дозволяє завантажувати та переглядати логи, графіки і звіти через інтерфейс GitHub.

#### 5. Підключення self-hosted runner
- Підключено локальний runner на ПК  
- Створено окремий workflow `ci-selfhosted.yml`, де запускаємо хоча б один модуль (`visualization`) на self-hosted runner  
- Збереження артефактів здійснюється через `upload-artifact`

### Гілки репозиторію
- `main`  
- `feature/ci_setup`  
- `feature/ci_selfhosted`  

### Git log
```text
* a1b2c3d (HEAD -> main, origin/main) Add CI workflow ci.yml
* e4f5g6h Add job run-modules with matrix setup
* i7j8k9l Add upload-artifact step for logs
* m0n1o2p Setup self-hosted workflow ci-selfhosted.yml
