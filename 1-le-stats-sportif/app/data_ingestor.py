import pandas as pd


class DataIngestor:
    def __init__(self, csv_path: str):
        self.data = pd.read_csv(csv_path)