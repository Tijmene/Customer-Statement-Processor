# Customer-Statement-Processor
This customer statement processor processes and validates customer statement records. Input can be in the CSV or XML file format.

## Install requirements.txt in venv
Open a terminal in the root of the Customer-Statement-Processor and create an environment by typing in the following commands:
1. py -m venv Customer-Statement-Processor
2. Activate the venv by executing the activate.bat -> venv\scripts\activate.bat
3. py -m pip install -r requirements.txt

## Starting up the API
1. Open a terminal in the root of the project.
2. Start the api with the following uvicorn command:
   - uvicorn StatementProcessor.ProcessorMain:app --host 0.0.0.0 --port 5000
3. The API is now running at localhost/5000

## Post to the API
The API expects files in binary which you can post to it using cURL or a gui such as Postman. Postman API calls can be 
imported my importing from the StatementProcessor.postman_collection.json file. Postman has the advantage that is 
immediately visualizes the pdf file that is returned from the API.

Sometimes Postman clears the content-type. If this happens remove and re-add the file to be sent in Postman.

## Running without the API
It is possible to analyze files without the API by running the run_without_api.py file directly. 