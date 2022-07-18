import os.path

from fpdf import FPDF
import uuid
from datetime import datetime
from dataclasses import fields

from StatementProcessor.CustomerStatementModel import CustomerStatementModel
from StatementProcessor.StatementValidation import LabeledStatement, StatementValidation


def build_report(labeled_statements: [LabeledStatement]) -> str:
    # Create instance of FPDF class
    # Letter size paper, use inches as unit of measure
    pdf = FPDF(format='letter')
    pdf.add_page()

    # Set column width to 1 / (elements in statement + 1) of effective page width to distribute content
    epw = pdf.w - 2 * pdf.l_margin

    # Document title centered, 'B'old, 14 pt
    pdf.set_font('Arial', 'B', 20.0)
    pdf.cell(epw, 0.0, 'Processed Customer Statements', align='C')
    pdf.set_font("Arial", size=8)
    pdf.ln(20)

    th = pdf.font_size + 1

    col_widths = _calc_col_widths(epw, fields(CustomerStatementModel))

    # Create headers
    for field in fields(CustomerStatementModel):
        pdf.cell(col_widths[field.name], th, str(field.name), border=1, fill=False)
    pdf.cell(col_widths["validation"], th, str("validation"), border=1, fill=False)

    pdf.ln(th)

    for labeled_statement in labeled_statements:
        statement = labeled_statement.statement
        label = labeled_statement.label
        if label is StatementValidation.VALID:
            pdf.set_fill_color(207, 242, 202)

        elif label is StatementValidation.INCORRECT_MUT or label is StatementValidation.NON_UNIQUE_REF:
            pdf.set_fill_color(250, 107, 132)

        for field in fields(statement):
            value = getattr(statement, field.name)
            pdf.cell(col_widths[field.name], th, str(value), border=1, fill=True)

        pdf.cell(col_widths["validation"], th, str(label), border=1, fill=True)

        pdf.ln(th)

    # Line break equivalent to 4 lines
    pdf.ln(4 * th)

    title = f"{datetime.today().strftime('%Y-%m-%d')}-Processed_statements-{uuid.uuid4()}"
    file_path = os.path.join("..", "pdf_reports", title + ".pdf")
    print(f"Saving pdf at {file_path}")
    pdf.output(f"{file_path}")

    return file_path


def _calc_col_widths(epw: float, fields) -> dict:
    col_widths = {}
    for field in fields:
        len_modifier = 1
        if field.name == "reference":
            len_modifier = 0.5
        elif field.name in ["start_balance", "mutation", "end_balance"]:
            len_modifier = 0.6
        elif field.name == "account_number":
            len_modifier = 1.2
        elif field.name == "description":
            len_modifier = 1.4

        col_widths[field.name] = ((epw / len(fields) + 1) * len_modifier)

    remaining_epw = epw - sum(col_widths.values())
    col_widths["validation"] = (remaining_epw)
    return col_widths
