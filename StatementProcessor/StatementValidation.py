from enum import Enum
from dataclasses import dataclass

from StatementProcessor.CustomerStatementModel import CustomerStatementModel


class StatementValidation(Enum):
    """ Enum describing the possible validation results """
    VALID = "valid"
    NON_UNIQUE_REF = "id not unique"
    INCORRECT_MUT = "incorrect mutation"

    def __str__(self):
        return str(self.value)


@dataclass
class LabeledStatement:
    """ Simple wrapper around a :class:`CustomerStatementModel` that adds a :class:`StatementValidation` Label. """
    statement: CustomerStatementModel
    label: StatementValidation
