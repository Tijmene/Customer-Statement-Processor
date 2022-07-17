import io
import xmltodict
import pandas as pd
import json


def load_xml(xml_file):
    json = xmltodict.parse(xml_file)
    statements = json["records"]["record"]
    formatted_statements = []
    for statement in statements:
        formatted_statement = {}
        formatted_statement["Reference"] = str(statement["@reference"])
        formatted_statement["Account number"] = str(statement["accountNumber"])
        formatted_statement["Start Balance"] = float(statement["startBalance"])
        formatted_statement["Mutation"] = float(statement["mutation"])
        formatted_statement["Description"] = str(statement["description"])
        formatted_statement["End Balance"] = float(statement["endBalance"])
        formatted_statements.append(formatted_statement)

    return formatted_statements


def load_csv(csv_file) -> [dict]:
    io_string = io.StringIO(csv_file.decode("ISO-8859-1"))
    statements = pd.read_csv(io_string)
    return [json.loads(statements.loc[index].to_json()) for index in statements.index]
