import os

import pandas as pd

from app.models.gemma import Gemma
from app.utils.submit import generate_submit

def gen_files():
    solutions_train = pd.read_excel('./data/raw/train/solutions.xlsx')
    tasks_train = pd.read_excel('./data/raw/train/tasks.xlsx')
    tests_train = pd.read_excel('./data/raw/train/tests.xlsx')

    solutions_test = pd.read_excel('./data/raw/test/solutions.xlsx')
    tasks_test = pd.read_excel('./data/raw/test/tasks.xlsx')
    tests_test = pd.read_excel('./data/raw/test/tests.xlsx')
    df_train = solutions_train.merge(tasks_train.rename(columns={'id': 'task_id'}), on='task_id', how='left')
    df_test = solutions_test.merge(tasks_test.rename(columns={'id': 'task_id'}), on='task_id', how='left')

    unit_map_train = lambda row: tests_train[tests_train['task_id'] == row.task_id][['type', 'input', 'output']] \
        .rename(columns={'type': 'Тип теста', 'input': 'Вход', 'output': 'Верный вывод программы'}) \
        .to_string(index=False)
    unit_map_test = lambda row: tests_test[tests_test['task_id'] == row.task_id][['type', 'input', 'output']] \
        .rename(columns={'type': 'Тип теста', 'input': 'Вход', 'output': 'Верный вывод программы'}) \
        .to_string(index=False)

    df_train['unit_true'] = df_train.apply(unit_map_train, axis=1)
    df_test['unit_true'] = df_test.apply(unit_map_test, axis=1)
    df_test['author_comment'] = ''

    system = 'Вы учитель и вы должны на русском языке давать подсказки без прямых исправлений кода, поддерживая формальный и дружелюбный стиль общения'
    df_train['system'] = df_test['system'] = system

    df_train.set_index('id', inplace=True)
    df_test.set_index('id', inplace=True)

    df_train.to_csv('./data/raw/train/data_full.csv')
    df_test.to_csv('./data/raw/test/data_full.csv')

if __name__ == "__main__":
    print('Init')

    gen_files()

    gemma = Gemma()

    def predict(row: pd.Series) -> str:
        return gemma.ask(row)

    print('Starting generation...')
    generate_submit(
        test_solutions_path="./data/raw/test/data_full.csv",
        predict_func=predict,
        save_path="./data/processed/submission.csv",
        use_tqdm=True,
    )
