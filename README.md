![image](https://github.com/user-attachments/assets/678e6e14-ae3e-4aa6-a968-a81a333674e9)

# AI Assistant Hack: Python – Команда MMG

## Описание задачи
Необходимо разработать алгоритм, который будет подсказывать студентам, как поправить их Python код, чтобы он работал корректно.

Студенты, изучающие программирование на Python, периодически сталкиваются с трудностями при выполнении практических заданий. Особенно это проявляется при посылке задачи в тестирующую систему - открытые тесты пройдены, а вот закрытые - нет, и узнать их никак нельзя.

Мы хотим, чтобы алгоритм играл роль личного ментора, который сможет проанализировать код на предмет не только синтаксических ошибок (которые сможет выявить и среда разработки, и линтер, и др.), но и логические ошибки. Он будет направлять мысль в нужное русло, указывать на необходимость перепроверки какой-либо логики в коде, но не будет писать код за него.

## Ссылки
Репозиторий: https://github.com/werserk/hse-aiahp-baseline \
Тестирующая система: https://dsworks.ru/champ/hse-2024-october \
Лендинг: https://www.hse.ru/ai-assistant-hack-python/

## Состав
* **Денис Маликов** – Капитан, DA
* **Артём Таратин** – DS
* **Даниил Аль-Натор** – DS
* **Илья Обухов** – DE
* **Максим Чудасов** – PM

## Место в топе по метрике
Паблик | Приват
---|---
<img width="655" alt="Снимок экрана 2024-10-24 в 10 59 43" src="https://github.com/user-attachments/assets/26da6c73-9004-47c4-856a-58416e4ae644"> | <img width="653" alt="Снимок экрана 2024-10-24 в 11 00 31" src="https://github.com/user-attachments/assets/ae01dca0-9a79-4a1d-9923-e3fdb8915126">

## Загрузка
```bash
git clone https://github.com/kekwak/HSE-AI-Assistant-Hack.git
cd HSE-AI-Assistant-Hack
```

## Запуск в контейнере
Собрать контейнер самому:
```bash
docker build -t kekwak/docker-app:latest .
docker run -v "$(pwd):/app" -v "$(pwd)/data:/app/data" -p 8000:8000 --gpus all --rm kekwak/docker-app:latest
```
или скачать готовый образ:
```bash
docker compose up --pull always
```
а также запуск через альтернативный докерфайл:
```bash
docker build -f Dockerfile-conda -t kekwak/docker-app:latest-conda .
docker run -v "$(pwd):/app" -v "$(pwd)/data:/app/data" -p 8000:8000 --gpus all --rm kekwak/docker-app:latest-conda
```

## Запуск в локальной среде
В проекте исспользуется анаконда.
* При установке зависимостей этим способом могут возникнуть проблемы.

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
│   ├── __init__.py
│   ├── models   <------------------------ Подключаемые модели
│   │   ├── base.py
│   │   ├── gemma.py
│   │   ├── __init__.py
│   │   └── yandexgpt.py
│   └── utils    <------------------------ Утилиты
│       ├── __init__.py
│       ├── metric.py <------------------------ Ознакомьтесь с метрикой
│       └── submit.py <------------------------ Здесь всё для генерации сабмита
├── data
│   ├── complete
│   ├── processed <----------------------- Подготовленные данные, сабмиты
│   └── raw <----------------------------- Исходные данные
│       ├── submit_example.csv
│       ├── test
│       │   ├── solutions.xlsx
│       │   ├── tasks.xlsx
│       │   └── tests.xlsx
│       └── train
│           ├── solutions.xlsx
│           ├── tasks.xlsx
│           └── tests.xlsx
├── docker-compose.yaml
├── Dockerfile <----------------------- Докерфайл для запуска в контейнере
├── Dockerfile-conda
├── environment.yml
├── gemma-2-9b-0.7846-12 <------------- Модель
│   ├── adapter_config.json
│   ├── adapter_model.safetensors
│   ├── README.md
│   ├── special_tokens_map.json
│   ├── tokenizer_config.json
│   ├── tokenizer.json
│   └── tokenizer.model
├── .gitattributes
├── .gitignore
├── main.py <---------------------------- [ВАЖНО] Именно этот скрипт мы будем запускать при проверке ваших решений. Он должен генерировать финальный сабмит.
├── notebooks
│   └── yandexgpt.ipynb
│   └── train-model.ipynb <-------------- Обучение модели
│   └── analys.ipynb <------------------- Анализ
├── README.md <-------------------------- Инструкция
└── tests
    ├── test_correctness.py <------------------------ Проверить сабмит на корректность
    └── test_embedding_generation.py <--------------- Попробовать генерацию эмбеддингов и подсчёт метрики
```
