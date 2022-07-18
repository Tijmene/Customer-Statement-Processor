import os

import uvicorn
from fastapi import FastAPI, Request, HTTPException

# Using dotenv to load environment variables.
from dotenv import load_dotenv

# Using existing module to specify location of the .env file
# The variables are pushed to git, normally they are not on the repository for safety reasons.
from pathlib import Path

from starlette.responses import FileResponse

from StatementProcessor.ReportBuilder import build_report
from StatementProcessor.StatementProcessorLogic import evaluate_statements
from StatementProcessor.FileLoader import load_xml, load_csv

load_dotenv()
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

ROOT_DIR = os.path.abspath(os.path.join(__file__, "..", ".."))

app = FastAPI()

@app.post("/validate-statement-file")
async def validate(request: Request):

    content_type = request.headers['Content-Type']
    file = await request.body()
    if content_type == 'application/xml':
        customer_statements = load_xml(file)
    elif content_type == 'text/csv' or content_type == 'application/csv':
        customer_statements = load_csv(file)
    else:
        raise HTTPException(status_code=400, detail=f'Content type {content_type} is not supported. '
                                                    f'Please post in either csv or xml.\n'
                                                    f'If you are unsure what to do please contact the admin '
                                                    f'{os.environ["ADMIN_EMAIL"]}')
    labeled_statements = evaluate_statements(statements=customer_statements)

    report_pdf_location = await build_report(labeled_statements)

    return FileResponse(report_pdf_location,
                        media_type="application/pdf",
                        filename="ticket.pdf")


if __name__ == "__main__":
    print(ROOT_DIR)
    uvicorn.run("ProcessorMain:app",
                host='0.0.0.0',
                port=5000,
                reload=True,
                debug=True,
                workers=1)



