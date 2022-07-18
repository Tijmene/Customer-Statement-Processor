import io
import xmltodict
import pandas as pd
import json
from StatementProcessor.CustomerStatementModel import CustomerStatementModel


def load_xml(xml_file) -> [CustomerStatementModel]:
    """
    Loads the statements from a xml file to :class:`CustomerStatementModel`s.
    :param xml_file: binary of the xml file
    :return: list of :class:`CustomerStatementModel`
    """
    json = xmltodict.parse(xml_file)
    statements = json["records"]["record"]
    statement_models = []
    for statement in statements:
        statement_models.append(CustomerStatementModel(statement))
    return statement_models


def load_csv(csv_file) -> [CustomerStatementModel]:
    """
    Loads the statements from a csv file to :class:`CustomerStatementModel`s.
    :param csv_file: binary of the csv file
    :return: list of :class:`CustomerStatementModel`
    """
    io_string = io.StringIO(csv_file.decode("ISO-8859-1"))
    statements = pd.read_csv(io_string)
    statement_models = []
    for statement in [json.loads(statements.loc[index].to_json()) for index in statements.index]:
        statement_models.append(CustomerStatementModel(statement))
    return statement_models
