

import pandas as pd


class CSVProcessor:

    @staticmethod
    def read_csv(file):

        return pd.read_csv(file)

    @staticmethod
    def clean_data(df):

        df = df.drop_duplicates()

        return df

    @staticmethod
    def convert_types(df):

        df["timestamp"] = pd.to_datetime(df["timestamp"])

        return df