import random
from functional import seq
import pandas as pd
import collections

from StatementProcessor.StatementValidation import StatementValidation, LabeledStatement
from StatementProcessor.CustomerStatementModel import CustomerStatementModel, generate_random_csm


def evaluate_statements(statements: [CustomerStatementModel]) -> [LabeledStatement]:
    """
    Checks incoming statements for validity by checking if all have a unique reference id
    and if the mutation had the desired effect on the account balance.
    :param statements: :class:`CustomerStatementModel` description of the customer statement.
    :return: :class:`LabeledStatement` Each statement labeled as either being valid or invalid
    with a specific reason.
    """
    labeled_statements = []
    all_ids = [statement.reference for statement in statements]
    duplicate_ids = [x for x, y in collections.Counter(all_ids).items() if y > 1]

    for statement in statements:
        # Check if reference id is unique
        labels = []
        if statement.reference in duplicate_ids:
            labels.append(StatementValidation.NON_UNIQUE_REF)
        # Check if the mutation was processed correctly
        if not _mutation_ok(statement):
            labels.append(StatementValidation.INCORRECT_MUT)
        if len(labels) == 0:
            labels.append(StatementValidation.VALID)
        labeled_statements.append(LabeledStatement(statement, labels))

    return labeled_statements


def _mutation_ok(statement: CustomerStatementModel) -> bool:
    return round(statement.start_balance + statement.mutation, 2) == statement.end_balance


def test_identical_references():
    num_same_id = random.randint(1, 500)
    identical_id = str(random.randint(1, 100000))
    models = []
    for i in range(1000):
        if i < num_same_id:
            model = generate_random_csm(reference=identical_id,
                                        correct_mut=True)
        else:
            model = generate_random_csm(correct_mut=True)
        models.append(model)

    labeled_models = evaluate_statements(models)
    number_of_non_uniques = \
        seq(labeled_models).map(lambda m: True if StatementValidation.NON_UNIQUE_REF in m.labels else False) \
                           .filter(lambda b: b) \
                           .len()

    assert number_of_non_uniques == num_same_id


def test_wrong_mutation():
    num_wrong_mut = random.randint(1, 500)
    models = []
    for i in range(1000):
        if i < num_wrong_mut:
            model = generate_random_csm(correct_mut=False)
        else:
            model = generate_random_csm(correct_mut=True)
        models.append(model)

    labeled_models = evaluate_statements(models)
    number_of_incorrect_muts = \
        seq(labeled_models).map(lambda m: True if StatementValidation.INCORRECT_MUT in m.labels else False) \
                           .filter(lambda b: b) \
                           .len()

    assert number_of_incorrect_muts == num_wrong_mut


def test_both_wrong():
    num_wrong_mut = random.randint(1, 500)
    num_same_id = random.randint(1, 500)
    identical_id = str(random.randint(1, 100000))
    models = []
    for i in range(1000):
        flag = False if i < num_wrong_mut else True
        ref = identical_id if i < num_same_id else None

        model = generate_random_csm(correct_mut=flag, reference=ref)
        models.append(model)

    labeled_models = evaluate_statements(models)
    number_of_incorrect_muts = \
        seq(labeled_models).map(lambda m: True if StatementValidation.INCORRECT_MUT in m.labels else False) \
                           .filter(lambda b: b) \
                           .len()

    number_of_non_uniques = \
        seq(labeled_models).map(lambda m: True if StatementValidation.NON_UNIQUE_REF in m.labels else False) \
                           .filter(lambda b: b) \
                           .len()

    assert number_of_non_uniques == num_same_id
    assert number_of_incorrect_muts == num_wrong_mut

if __name__ == "__main__":
    import json

    csv_path = "../incoming_statements/records.csv"
    with open(csv_path, encoding="ISO-8859-1") as file:
        statements = pd.read_csv(file)
        statements = [CustomerStatementModel(json.loads(statements.loc[index].to_json()))
                      for index in statements.index]

    labeled_transactions = evaluate_statements(statements)
    print(labeled_transactions)
