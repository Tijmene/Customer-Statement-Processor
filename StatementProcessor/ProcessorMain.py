import os
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from starlette.responses import FileResponse

from StatementProcessor.ReportBuilder import build_report
from StatementProcessor.ProcessorLogic import evaluate_statements
from StatementProcessor.FileLoader import load_xml, load_csv

# Loading environment variables using dotenv.
# The variables are pushed to git, normally they are not on the repository for safety reasons.
from dotenv import load_dotenv
ROOT_DIR = os.path.abspath(os.path.join(__file__, "..", ".."))
load_dotenv(os.path.join(ROOT_DIR, ".env"))
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

app = FastAPI()


@app.post("/validate-statement-file")
async def validate(request: Request):
    """
    This endpoint processes and validates xml or csv documents that are posted to it.
    :param request: the incoming request which should contain the file.
    :return: A PDF showing the result of the validation.
    """

    # We first convert the incoming data to CustomerStatementModel s
    content_type = request.headers['Content-Type']
    file = await request.body()  # TODO save incom\ming files to the disk of the server (use same UUID as pdf)
    if content_type == 'application/xml':
        customer_statements = load_xml(file)
    elif content_type == 'text/csv' or content_type == 'application/csv':
        customer_statements = load_csv(file)
    else:
        raise HTTPException(status_code=400, detail=f'Content type {content_type} is not supported. '
                                                    f'Please post in either csv or xml.\n'
                                                    f'If you are unsure what to do please contact the admin '
                                                    f'{ADMIN_EMAIL}')
    # We evaluate the statements.
    labeled_statements = evaluate_statements(statements=customer_statements)

    # Create a pdf with the results
    report_pdf_location = build_report(labeled_statements)

    # And return the pdf.
    return FileResponse(report_pdf_location,
                        media_type="application/pdf",
                        filename="ticket.pdf")


if __name__ == "__main__":
    uvicorn.run("ProcessorMain:app",
                host='0.0.0.0',
                port=5000,
                reload=True,
                debug=True,
                workers=1)



