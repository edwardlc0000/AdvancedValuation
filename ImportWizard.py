import pandas as pd
import wx
from pathlib import Path

def import_statements() -> pd.DataFrame:
    
    
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
        print("No file selected.")
        dialog.Destroy()
        app.Destroy()
        return {}

    dialog.Destroy()
    app.Destroy()

    file_path: Path = Path(file_name)
    
    df = pd.read_xlsx(file_path)

    return df


if __name__ == "__main__":
    df = import_statements()
    print(df.head())
