import pandas as pd
import collections


def validate_statements(statements: [dict]) -> [dict]:
    """
    Validates incoming statements by checking if all have a unique reference id
    and if the mutation had the desired effect on the account balance.
    :param statements: A list of dictionaries in which each dictionary is a representation
    of a payment statement.
    :return: a list of statement descriptions that have failed validation.
    """
    failed_statements = []
    all_ids = [statement["Reference"] for statement in statements]
    duplicate_ids = [x for x, y in collections.Counter(all_ids).items() if y > 1]

    for statement in statements:
        # Check if reference id is unique
        if statement["Reference"] in duplicate_ids:
            failed_statements.append(statement)
            continue

        # Check if the mutation was processed correctly
        if not _mutation_ok(start=statement["Start Balance"],
                            mutation=statement["Mutation"],
                            end=statement["End Balance"]):
            failed_statements.append(statement)
            continue

    return failed_statements


def _mutation_ok(start: float, mutation: float, end: float) -> bool:
    return round(start + mutation, 2) == end


if __name__ == "__main__":
    import json

    csv_path = "../incoming_statements/records.csv"
    with open(csv_path, encoding="ISO-8859-1") as file:
        statements = pd.read_csv(file)
        statements = [json.loads(statements.loc[index].to_json()) for index in statements.index]
    failed_transactions = validate_statements(statements)
