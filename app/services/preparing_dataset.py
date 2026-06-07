import pandas as pd
import re
import unicodedata

def convert_clean_dataset(path: str = "data_test/full_dataset_incident.xlsx"):
    use_cols = ["ID", "Дата создания", "Группа тем", "Тема", "Муниципалитет", "Населенный пункт", "Текст инцидента"]
    df = pd.read_excel(path, engine="openpyxl", usecols=use_cols)

    df.to_parquet("/home/faster/ProjectsPy/Income/data_test/data_prepair.parquet")
    return df

a = convert_clean_dataset()

