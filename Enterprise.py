# A class modeling the financial statements of an enterprise

import pandas as pd

class Enterprise:

    def __init__(self, name: str, ticker: str, fdso: int,
                 income_statement: pd.DataFrame,
                 cash_flow_statement: pd.DataFrame,
                 balance_sheet: pd.DataFrame):
        self.name: str = name
        self.ticker: str = ticker
        self.fdso: int = fdso
        self.income_statement: pd.DataFrame = income_statement
        self.cash_flow_statement: pd.DataFrame = cash_flow_statement
        self.balance_sheet: pd.DataFrame = balance_sheet





