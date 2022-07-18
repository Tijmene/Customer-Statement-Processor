import uvicorn
import requests as r
from fastapi import FastAPI, Request, HTTPException, Response

# Using dotenv to load environment variables.
from dotenv import load_dotenv

# Using existing module to specify location of the .env file
# The variables are pushed to git, normally they are not on the repository for safety reasons.
from pathlib import Path

from StatementProcessor.StatementProcessorLogic import validate_statements
from FileLoader import load_xml, load_csv

load_dotenv()
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

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
        raise HTTPException(status_code=400, detail=f'Content type {content_type} not supported. '
                                                    f'Please post in either csv or xml.')
    failed_statements = validate_statements(statements=customer_statements)

    return Response(content=failed_statements)

if __name__ == "__main__":
    uvicorn.run("ProcessorMain:app",
                host='0.0.0.0',
                port=5000,
                reload=True,
                debug=True,
                workers=1)

