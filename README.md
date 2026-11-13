# Steam Games Analytics

## Описание проекта

Проект посвящён исследовательскому анализу данных об играх платформы Steam и автоматизированной обработке данных с последующей загрузкой в PostgreSQL.

Проект включает два основных направления:

- **EDA (Exploratory Data Analysis):** исследование структуры, качества, распределений и взаимосвязей в данных.
- **ETL (Extract, Transform, Load):** автоматизированная загрузка, преобразование, проверка и сохранение данных в PostgreSQL.

## Структура проекта

```text
Steam-Games-Analytics/
│
├── notebooks/
│   └── EDA.ipynb
│
├── src/
│   └── etl/
│       ├── download.py
│       ├── extract.py
│       ├── transform.py
│       ├── validate.py
│       ├── load.py
│       └── main.py
│
├── tests/
│   └── test_etl.py
│
├── datasets/              # Локальные данные (не включены в Git)
├── pyproject.toml
├── .gitignore
└── README.md
```

## 1. Исходные данные

Используется [Steam Games Dataset](https://drive.google.com/file/d/1vpHJJoH_e0UwlueVYfMfPD_ViFNoS1RI/view).

- Формат: Parquet.
- Количество записей: 125 855.
- Используемые признаки: `AppID`, `Name`, `Price`, `Positive`, `Negative`.

Датасет автоматически загружается из Google Drive, если локальная копия отсутствует.

## 2. Исследовательский анализ (EDA)

Анализ представлен в `notebooks/EDA.ipynb`.

Основные направления:
- Исследование структуры и качества данных.
- Анализ пропущенных значений и выбросов.
- Изучение распределений и категориальных переменных.
- Анализ корреляций.
- Визуализация результатов.

Используемые библиотеки: pandas, NumPy, Matplotlib, Seaborn.

## 3. ETL-процесс

ETL реализован в виде модульного Python-пакета.

| Этап | Описание |
|---|---|
| Download | Загрузка датасета из Google Drive при отсутствии локального файла |
| Extract | Чтение Parquet и проверка структуры данных |
| Transform | Очистка данных, удаление дубликатов и отбор до 100 записей |
| Validate | Проверка типов, пропусков, уникальности и допустимых значений |
| Load | Загрузка и обновление записей в PostgreSQL |

Для загрузки используются `AppID` в качестве первичного ключа и механизм `ON CONFLICT DO UPDATE`.

## 4. Установка и запуск

**Требования:** Python 3.10+, PostgreSQL и предоставленный преподавателем файл `creds.db`.

Клонирование репозитория:

```bash
git clone https://github.com/MDeeb88/Data-Engineering-Project_Steam-Games-Analytics.git

cd Data-Engineering-Project_Steam-Games-Analytics
```

Создание виртуального окружения:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Установка зависимостей:

```bash
python -m pip install -e .
python -m pip install --group dev
```

Поместите `creds.db` в корневую директорию проекта. Датасет вручную скачивать не требуется.

**Запуск EDA:**

```bash
jupyter notebook
```

Откройте `notebooks/EDA.ipynb`.

**Запуск ETL:**

```bash
python -m etl.main --table deebm
```

Дополнительные аргументы:

- `--dataset` — путь к Parquet-файлу.
- `--creds` — путь к SQLite с учётными данными.
- `--table` — название целевой таблицы PostgreSQL.

## 5. Результаты

| Показатель | Результат |
|---|---:|
| Исходные записи | 125 855 |
| Обработанные записи | 125 855 |
| Отобранные записи | 100 |
| Проверенные записи | 100 |
| Загруженные записи в PostgreSQL | 100 |
| Успешные автоматизированные тесты | 9/9 |

Дополнительно проверены автоматическая загрузка датасета из Google Drive, установка проекта в чистом виртуальном окружении и качество кода с помощью Ruff.

## 6. Тестирование

Запуск автоматизированных тестов:

```bash
python -m pytest -v
```

Проверка качества кода:

```bash
ruff check src tests
ruff format --check src tests
```

## Используемые технологии

Python, pandas, NumPy, PyArrow, Matplotlib, Seaborn, Jupyter Notebook, PostgreSQL, SQLite, psycopg2, gdown, pytest, Ruff.

## Безопасность

Локальные датасеты, `creds.db`, виртуальные окружения и временные файлы исключены из Git с помощью `.gitignore`.

Учётные данные не хранятся в исходном коде и не публикуются в репозитории.