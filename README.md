# Customer-Statement-Processor
This customer statement processor processes and validates customer statement records. Input can be in the CSV or XML file format. 

## Install requirements.txt in venv
Open a terminal in the root of the Customer-Statement-Processor and create an environment by typing in the following commands:
1. py -m venv Customer-Statement-Processor
2. Activate the venv by executing the activate.bat -> venv\scripts\activate.bat
3. py -m pip install -r requirements.txt

## Starting up the API
1. Open a terminal in the root of the project.
2. Start uvicorn with the following command:
   - uvicorn StatementProcessor.ProcessorMain:app --host 0.0.0.0 --port 5000
3. The API is now running at localhost/5000