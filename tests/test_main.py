import os
import pandas as pd

from solsquad_bootcamp.main import read_csv_to_df


def test_read_csv_to_df_loads_dataframe():
    # tests/ -> project root is parent
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    path = os.path.join(repo_root, "data", "mock-data.csv")

    df = read_csv_to_df(path)

    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] > 0
    # ensure expected columns exist
    expected = {"name", "email", "phone", "birthdate", "data"}
    assert expected.issubset(set(df.columns))
