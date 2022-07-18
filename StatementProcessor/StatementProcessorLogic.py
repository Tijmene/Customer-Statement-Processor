import pandas as pd
import collections
from StatementProcessor.CustomerStatementModel import CustomerStatementModel


def validate_statements(statements: [CustomerStatementModel]) -> [CustomerStatementModel]:
    """
    Validates incoming statements by checking if all have a unique reference id
    and if the mutation had the desired effect on the account balance.
    :param statements: :class:`CustomerStatementModel` description of the customer statement.
    :return: A list if :class:`CustomerStatementModel` that failed the validation.
    """
    failed_statements = []
    all_ids = [statement.reference for statement in statements]
    duplicate_ids = [x for x, y in collections.Counter(all_ids).items() if y > 1]

    for statement in statements:
        # Check if reference id is unique
        if statement.reference in duplicate_ids:
            failed_statements.append(statement)
            continue

        # Check if the mutation was processed correctly
        if not _mutation_ok(statement):
            failed_statements.append(statement)
            continue

    return failed_statements


def _mutation_ok(statement: CustomerStatementModel) -> bool:
    return round(statement.start_balance + statement.mutation, 2) == statement.end_balance


if __name__ == "__main__":
    import json

    csv_path = "../incoming_statements/records.csv"
    with open(csv_path, encoding="ISO-8859-1") as file:
        statements = pd.read_csv(file)
        statements = [CustomerStatementModel(json.loads(statements.loc[index].to_json()))
                      for index in statements.index]

    failed_transactions = validate_statements(statements)
