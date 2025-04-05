#

import pandas as pd
from pathlib import Path

na_values = ['', '#N/A', '#N/A N/A', '#NA',
             '-1.#IND', '-1.#QNAN', '-NaN',
             '-nan', '1.#IND', '1.#QNAN',
             '<NA>', 'N/A', 'NA', 'NULL',
             'NaN', 'None', 'n/a', 'nan',
             'null']

is_start: int = 9
is_len: int = 175
cf_start: int = 185
cf_len: int = 94
bs_start: int = 280

# noinspection PyTypeChecker
def import_statements(stmt: str, file_name: str) -> pd.DataFrame:

    file_path: Path = Path(file_name)

    match stmt:
        case "is":
            df: pd.DataFrame = pd.read_excel(file_path,
                                             sheet_name="Financial Statements",
                                             index_col=0,
                                             header=0,
                                             skiprows=is_start,
                                             nrows=is_len,
                                             usecols=range(0, 11),
                                             na_values=na_values)
        case "cf":
            df: pd.DataFrame = pd.read_excel(file_path,
                                             sheet_name="Financial Statements",
                                             index_col=0,
                                             header=0,
                                             skiprows=cf_start,
                                             nrows=cf_len,
                                             usecols=range(0, 11),
                                             na_values=na_values)
        case "bs":
            df: pd.DataFrame = pd.read_excel(file_path,
                                             sheet_name="Financial Statements",
                                             index_col=0,
                                             header=0,
                                             skiprows=bs_start,
                                             usecols=range(0, 11),
                                             na_values=na_values)
        case _:
            raise ValueError("Invalid statement type.")

    return df


if __name__ == "__main__":
    test_df = import_statements('is', 'IBM.xlsx')
    print(test_df.head(10))
