import random
import string
from dataclasses import dataclass


@dataclass
class CustomerStatementModel:
    """
    Representation of a customer statement.
    """
    reference: str
    account_number: str
    start_balance: float
    mutation: float
    end_balance: float
    description: str

    def __init__(self, statement_dict: dict):
        missing_keys = []

        if "@reference" in statement_dict:
            key_ref = "@reference"
        elif "Reference" in statement_dict:
            key_ref = "Reference"
        else:
            missing_keys.append("Reference")

        if "accountNumber" in statement_dict:
            key_acc = "accountNumber"
        elif "Account Number" in statement_dict:
            key_acc = "Account Number"
        else:
            missing_keys.append("Account Number")

        if "startBalance" in statement_dict:
            key_start = "startBalance"
        elif "Start Balance" in statement_dict:
            key_start = "Start Balance"
        else:
            missing_keys.append("Start Balance")

        if "mutation" in statement_dict:
            key_mut = "mutation"
        elif "Mutation" in statement_dict:
            key_mut = "Mutation"
        else:
            missing_keys.append("Mutation")

        if "endBalance" in statement_dict:
            key_end = "endBalance"
        elif "End Balance" in statement_dict:
            key_end = "End Balance"
        else:
            missing_keys.append("End Balance")

        if "description" in statement_dict:
            key_desc = "description"
        elif "Description" in statement_dict:
            key_desc = "Description"
        else:
            missing_keys.append("Description")

        if len(missing_keys) > 0:
            raise ValueError(f"The customer statement is incomplete! The following values are missing:\n"
                             f"{str(missing_keys).strip('[]')}")

        self.reference = str(statement_dict[key_ref])
        self.account_number = str(statement_dict[key_acc])
        self.start_balance = float(statement_dict[key_start])
        self.mutation = float(statement_dict[key_mut])
        self.description = str(statement_dict[key_desc])
        self.end_balance = float(statement_dict[key_end])


def generate_random_csm(correct_mut: bool = True,
                        reference: str = None,
                        account_number: str = None,
                        start_balance: float = None,
                        mutation: float = None,
                        end_balance: float = None,
                        description: str = None) -> CustomerStatementModel:
    if reference is None:
        reference = random.randint(1, 10000000)
    if account_number is None:
        account_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    if start_balance is None:
        start_balance = round(random.uniform(10, 10000.00), 2)
    if mutation is None:
        mutation = round(random.uniform(-1000.00, 1000.00), 2)
    if end_balance is None and correct_mut:
        end_balance = round(start_balance + mutation, 2)
    else:
        end_balance = round(random.uniform(-1000.00, 1000.00), 2)

    if description is None:
        description = ''.join(random.choices(string.ascii_uppercase + string.digits, k=30))
    return CustomerStatementModel({"Reference": reference,
                                   "Account Number": account_number,
                                   "Start Balance": start_balance,
                                   "Mutation": mutation,
                                   "End Balance": end_balance,
                                   "Description": description})
