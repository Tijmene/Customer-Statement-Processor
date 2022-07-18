import os

import requests

base_path = os.path.join("..", "test_statements")


def send_csv():
    with open(os.path.join(base_path, "records.csv"), mode='rb') as file:
        url = "http://0.0.0.0:5000/validate-statement-file"
        payload = file
        headers = {
            'Content-Type': 'application/xml'
        }

        return requests.request("POST", url, headers=headers, data=payload)


def send_xml():
    with open(os.path.join(base_path, "records.xml"), mode='rb') as file:
        url = "http://0.0.0.0:5000/validate-statement-file"
        payload = file
        headers = {
            'Content-Type': 'text/csv'
        }

        return requests.request("POST", url, headers=headers, data=payload)


if __name__ == "__main__":
    r = send_xml()
    r = send_csv()
    pass
