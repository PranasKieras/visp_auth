import subprocess
import os
import re

def get_auth_request_body():
    xml_pattern = re.compile(r'<authenticationRequest.*?</authenticationRequest>', re.DOTALL)
    return run_jar('/create_ticket/signature-test-0.0.1-SNAPSHOT.jar', xml_pattern)

def get_data_request_body(ticket_id):
    xml_pattern = re.compile(r'<authenticationDataRequest.*?</authenticationDataRequest>', re.DOTALL)
    return run_jar('/get_customer_data/signature-test-0.0.1-SNAPSHOT.jar', xml_pattern, ticket_id)

def run_jar(jar_path, xml_pattern, *args):
    full_path = os.getcwd() + jar_path
    command = ['java', '-jar', full_path] + list(args)

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        if result.stderr:
            print("Error from JAR:")
            print(result.stderr)

        match = xml_pattern.search(result.stdout)

        body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:xd="http://www.w3.org/2000/09/xmldsig#">
            <soapenv:Header/>
            <soapenv:Body>{result}</soapenv:Body>
            </soapenv:Envelope>""".format(result=match.group(0))

        return body

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing the JAR: {e}")
        print(f"Return code: {e.returncode}")
        if e.output:
            print("Output:", e.output)
        if e.stderr:
            print("Error:", e.stderr)
