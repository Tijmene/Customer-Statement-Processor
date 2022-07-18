import os.path

from fpdf import FPDF
import uuid
from datetime import datetime
from dataclasses import fields

from StatementProcessor.CustomerStatementModel import CustomerStatementModel
from StatementProcessor.StatementValidation import LabeledStatement, StatementValidation


async def build_report(labeled_statements: [LabeledStatement]) -> str:
    """
    Builds a pdf that details the result of the validation.
    :param labeled_statements: list of :class:`LabeledStatement's
    :return: the path where the pdf is stored.
    """

    # Create instance of FPDF class in Letter size paper
    pdf = FPDF(format='letter')
    pdf.add_page()

    # Set the effective page width
    epw = pdf.w - 2 * pdf.l_margin

    # Document title centered
    pdf.set_font('Arial', 'B', 20.0)
    pdf.cell(epw, 0.0, 'Processed Customer Statements', align='C')
    pdf.set_font("Arial", size=8)
    pdf.ln(20)

    # Space between rows and columns
    th = pdf.font_size + 1
    col_widths = _calc_col_widths(epw, fields(CustomerStatementModel))

    # Create headers
    for field in fields(CustomerStatementModel):
        pdf.cell(col_widths[field.name], th, str(field.name), border=1, fill=False)
    pdf.cell(col_widths["validation"], th, str("validation"), border=1, fill=False)

    pdf.ln(th)

    # Insert the data
    for labeled_statement in labeled_statements:
        statement = labeled_statement.statement
        labels = labeled_statement.labels
        if StatementValidation.VALID in labels:
            pdf.set_fill_color(207, 242, 202)

        elif StatementValidation.INCORRECT_MUT in labels or StatementValidation.NON_UNIQUE_REF in labels:
            pdf.set_fill_color(250, 107, 132)

        for field in fields(statement):
            value = getattr(statement, field.name)
            pdf.cell(col_widths[field.name], th, str(value), border=1, fill=True)

        labels = [str(label) for label in labels]
        pdf.cell(col_widths["validation"], th, str(labels).strip("[]"), border=1, fill=True)

        pdf.ln(th)

    # Line break equivalent to 4 lines
    pdf.ln(4 * th)

    # Save the generated pdf ensuring an unique name by using a uuid
    title = f"{datetime.today().strftime('%Y-%m-%d')}-Processed_statements-{uuid.uuid4()}"
    from StatementProcessor.ProcessorMain import ROOT_DIR
    file_path = os.path.join(ROOT_DIR, "pdf_reports", title + ".pdf")
    pdf.output(f"{file_path}")

    return file_path


def _calc_col_widths(epw: float, fields) -> dict:
    col_widths = {}
    for field in fields:
        len_modifier = 1
        if field.name == "reference":
            len_modifier = 0.45
        elif field.name in ["start_balance", "mutation", "end_balance"]:
            len_modifier = 0.55
        elif field.name == "account_number":
            len_modifier = 1.1
        elif field.name == "description":
            len_modifier = 1.4

        col_widths[field.name] = ((epw / len(fields) + 1) * len_modifier)

    remaining_epw = epw - sum(col_widths.values())
    col_widths["validation"] = (remaining_epw)
    return col_widths
