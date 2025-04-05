import pandas as pd
import wx
from pathlib import Path

na_values = ['', '#N/A', '#N/A N/A', '#NA',
             '-1.#IND', '-1.#QNAN', '-NaN',
             '-nan', '1.#IND', '1.#QNAN',
             '<NA>', 'N/A', 'NA', 'NULL',
             'NaN', 'None', 'n/a', 'nan',
             'null']


# noinspection PyTypeChecker
def import_statements(stmt: str) -> pd.DataFrame:

    app = wx.App(False)

    dialog = wx.FileDialog(
        None,
        "Select a File",
        wildcard="Excel Files (*.xlsx)|*.xlsx",
        style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    )

    if dialog.ShowModal() == wx.ID_OK:
        file_name = dialog.GetPath()
    else:
        dialog.Destroy()
        app.Destroy()
        raise FileNotFoundError("No file selected.")

    dialog.Destroy()
    app.Destroy()

    file_path: Path = Path(file_name)

    match stmt:
        case "is":
            df: pd.DataFrame = pd.read_excel(file_path,
                                             sheet_name="Financial Statements",
                                             index_col=0,
                                             header=9,
                                             skiprows=0,
                                             nrows=175,
                                             usecols=range(0, 11),
                                             na_values=na_values)
        case "cf":
            df: pd.DataFrame = pd.read_excel(file_path,
                                             sheet_name="Financial Statements",
                                             index_col=0,
                                             header=0,
                                             skiprows=185,
                                             nrows=94,
                                             usecols=range(0, 11),
                                             na_values=na_values)
        case "bs":
            df: pd.DataFrame = pd.read_excel(file_path,
                                             sheet_name="Financial Statements",
                                             index_col=0,
                                             header=0,
                                             skiprows=280,
                                             usecols=range(0, 11),
                                             na_values=na_values)
        case _:
            raise ValueError("Invalid statement type.")

    return df


if __name__ == "__main__":
    test_df = import_statements('is')
    print(test_df.head(10))
