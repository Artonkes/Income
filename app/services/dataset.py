from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from text_cleaner import clean_text

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Константы
# ---------------------------------------------------------------------------

# Нужные нам колонки
REQUIRED_COLUMNS = [
    "ID",
    "Дата создания",
    "Группа тем",
    "Тема",
    "Муниципалитет",
    "Населенный пункт",
    "Текст инцидента",
]

# Изменение навзания колонок, для более удобного использования в коде
COLUMN_RENAME_MAP = {
    "ID":               "id",
    "Дата создания":    "date_created",
    "Группа тем":       "topic_group",
    "Тема":             "topic",
    "Муниципалитет":    "municipality",
    "Населенный пункт": "locality",
    "Текст инцидента":  "incident_text",
}


# ---------------------------------------------------------------------------
# Загрузка и первичная обработка
# ---------------------------------------------------------------------------

def load_raw(filepath: str | Path) -> pd.DataFrame:
    """
    Читает файл .xlsx и возвращает pd.DataFrame с нужными нам колонками
    """
    filepath = Path(filepath)
    logger.info("Загружаем файл: %s", filepath)

    df = pd.read_excel(filepath, engine="openpyxl")
    logger.info("Загружено строк: %d, колонок: %d", len(df), len(df.columns))

    # Проверка на наличие нужных колонок
    missing = []
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            missing.append(col)

    if missing:
        raise ValueError(f"В НАШЕМ ФАЙЛЕ ОТСУТСТВУЮТ КОЛОНКИ: {missing}")

    # Убираем все лишние колонки и оставляем нужные
    df = df[REQUIRED_COLUMNS].copy()
    df.rename(columns=COLUMN_RENAME_MAP, inplace=True)

    logger.info("Оставленые колонки: %d", df.columns)
    return df


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Очищаем весь текст из колонки incident_text при помощи функции clean_text
    """
    logger.info("Начинаем очистку текста...")

    df["incident_text"] = df["incident_text"].apply(clean_text)

    before = len(df)
    # Удаляем строки которые стали пустыми после отчистки
    df = df[df["incident_text"].str.len() > 0].copy()
    after = len(df)

    logger.info("Удалено строк с пустым текстом: %d", before - after)
    logger.info("Итого строк после очистки: %d", after)

    return df


