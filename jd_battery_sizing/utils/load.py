import os
import re
import pandas as pd

from config import Config, logger


def load_data():
    """
    Load and wrangle data
    """
    logger.info('Load Data')
    load_path = os.path.join(Config.DATA_DIR, 'SG200 KW Meter Data 2017_2020.xlsx')
    df = pd.read_excel(load_path)
    # Rename columns
    column_map = {col: re.sub('\)', '_', re.sub('\(', '_', re.sub(' ', '', col))) for col in df.columns}
    df = df.rename(columns=column_map)
    logger.info('Parse timestamp')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'].str.replace('@', ' '))

    return df
