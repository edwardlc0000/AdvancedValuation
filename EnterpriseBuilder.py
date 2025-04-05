#

import numpy as np

from Enterprise import Enterprise
from ImportWizard import import_statements

class EnterpriseBuilder:
    def __init__(self,
                 name: str, ticker: str, fdso: int,
                 debt_value: np.float64,
                 file_name: str):
        self.enterprise: Enterprise = Enterprise(name, ticker, fdso, debt_value)
        self.file_name: str = file_name

    def build(self):
        self.enterprise.income_statement = import_statements(stmt='is', file_name=self.file_name)
        self.enterprise.cash_flow_statement = import_statements(stmt='cs', file_name=self.file_name)
        self.enterprise.balance_sheet = import_statements(stmt='bs', file_name=self.file_name)
        return self.enterprise