from enum import Enum
from dataclasses import dataclass

from StatementProcessor.CustomerStatementModel import CustomerStatementModel


class StatementValidation(Enum):
    VALID = "valid"
    NON_UNIQUE_REF = "id not unique"
    INCORRECT_MUT = "incorrect mutation"

    def __str__(self):
        return str(self.value)


@dataclass
class LabeledStatement:
    statement: CustomerStatementModel
    label: StatementValidation
