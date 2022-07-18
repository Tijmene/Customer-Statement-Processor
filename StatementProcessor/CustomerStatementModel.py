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

