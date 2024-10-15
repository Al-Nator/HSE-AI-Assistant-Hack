# Команда MMG (MMGroup) – AI Assistant Hack: Python

## Состав
* **Капитан Денис Маликов** – Капитан, DA
* **Артём Таратин** – DS
* **Даниил Аль-Натор** – DS
* **Илья Обухов** – DE
* **Максим Чудасов** – PM

## Ссылки

Репозиторий: https://github.com/werserk/hse-aiahp-baseline \
Тестирующая система: https://dsworks.ru/champ/hse-2024-october \
Лендинг: https://www.hse.ru/ai-assistant-hack-python/

## Запуск в контейнере

```bash
docker compose up
```
или
```bash
docker build -t kekwak/docker-app:latest .
docker run -v "$(pwd):/app" -v "$(pwd)/data:/app/data" -p 8000:8000 --gpus all --rm kekwak/docker-app:latest
```

## Запуск в локальной среде

В проекте исспользуется анаконда

```bash
conda env create -f environment.yml
conda run -n unsloth_env pip install "unsloth @ git+https://github.com/unslothai/unsloth.git@79a2112ca4a775ce0b3cb75f5074136cb54ea6df"
conda run -n unsloth_env pip install --no-deps trl peft accelerate bitsandbytes
conda run -n unsloth_env pip install transformers==4.45.1 --force-reinstall
conda activate unsloth_env && python3 main.py
```

## Структура проекта

```
.
├── app
│   ├── __init__.py
│   ├── models   <------------------------ подключаемые модели
│   │   ├── base.py
│   │   ├── __init__.py
│   │   └── yandexgpt.py
│   └── utils    <------------------------ утилиты
│       ├── __init__.py
│       ├── metric.py <------------------------ ознакомьтесь с метрикой
│       └── submit.py <------------------------ здесь всё для генерации сабмита
├── data
│   ├── complete <------------------------ подготовленные данные, сабмиты
│   ├── processed <----------------------- промежуточный этап подготовки данных
│   └── raw <----------------------------- исходные данные
│       ├── submit_example.csv
│       ├── test
│       │   ├── solutions.xlsx
│       │   ├── tasks.xlsx
│       │   └── tests.xlsx
│       └── train
│           ├── solutions.xlsx
│           ├── tasks.xlsx
│           └── tests.xlsx
├── main.py <---------------------------- [ВАЖНО] Именно этот скрипт мы будем запускать при проверке ваших решений. Он должен генерировать финальный сабмит.
├── notebooks
│   └── yandexgpt.ipynb
├── poetry.lock
├── pyproject.toml
├── README.md
└── tests
    ├── test_correctness.py <------------------------ проверить на корректность сабмит
    └── test_embedding_generation.py <--------------- попробовать генерацию эмбеддингов и подсчёт метрики
```