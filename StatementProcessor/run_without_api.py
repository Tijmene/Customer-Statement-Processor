import json
import os
import pandas as pd

from StatementProcessor.CustomerStatementModel import CustomerStatementModel
from StatementProcessor.FileLoader import load_xml
from StatementProcessor.ProcessorLogic import evaluate_statements
from StatementProcessor.ReportBuilder import build_report


def analyze_csv():
    with open(os.path.join("..", "test_statements", "records.csv"), encoding="ISO-8859-1") as file:
        statements = pd.read_csv(file)
        statements = [CustomerStatementModel(json.loads(statements.loc[index].to_json()))
                      for index in statements.index]

        # We evaluate the statements.
        labeled_statements = evaluate_statements(statements=statements)

        # Create a pdf with the results
        pdf_loc = build_report(labeled_statements)
        return pdf_loc


def analyze_xml():
    with open(os.path.join("..", "test_statements", "records.xml"), mode='rb') as file:
        customer_statements = load_xml(file)

        # We evaluate the statements.
        labeled_statements = evaluate_statements(statements=customer_statements)

        # Create a pdf with the results
        pdf_loc = build_report(labeled_statements)
        return pdf_loc


if __name__ == "__main__":
    pdf_loc = analyze_csv()
    print(f"Analyzed csv, pdf can be found at {pdf_loc}")

    pdf_loc = analyze_xml()
    print(f"Analyzed xml, pdf can be found at {pdf_loc}")


