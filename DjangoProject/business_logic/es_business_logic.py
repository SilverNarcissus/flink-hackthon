import re
import subprocess
import tempfile
from django.http import JsonResponse

def submit_job(sql_query):
    # Step 2: Create a temporary file and write the SQL in it
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.sql') as temp_file:
        temp_file.write(sql_query)
        temp_file_path = temp_file.name

    # Step 3: Execute the `./bin/sql-client.sh -f <temp file>` command in the terminal
    command = f'~/Desktop/flink/flink-1.20.0/bin/sql-client.sh -f {temp_file_path}'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        return JsonResponse({'error': stderr.decode('utf-8')}, status=500)

    # Step 4: Wait for the command to execute and get the job ID from the output
    # Assuming the job ID is in the stdout
    output = stdout.decode('utf-8').strip()

    print("output: {}".format(output))
    print("Temp file: {} ".format(temp_file_path))

    return output

def extract_job_id(output):
    # Use regular expression to find the job ID in the output
    match = re.search(r'Job ID: (\w+)', output)
    if match:
        return match.group(1)
    else:
        return None

def table_to_json(output):
    import json

    # Regular expression to find the table part in the logs
    pattern = re.compile(r'\+----\+.*?Received', re.DOTALL)

    # Find the table part in the logs
    match = pattern.search(output)
    # Split the string into lines
    table_string = match.group(0)

    # Split the string into lines
    lines = table_string.strip().split('\n')

    # Extract the header and data lines
    header_line = lines[1]
    data_lines = lines[3:-2]

    # Split the header line into columns
    headers = [header.strip() for header in header_line.split('|')]

    # Initialize a list to hold the JSON objects
    json_list = []

    # Process each data line
    for data_line in data_lines:
        # Split the data line into columns
        data = [value.strip() for value in data_line.split('|')]
        # Create a dictionary from the headers and data
        result = {headers[i]: data[i] for i in range(2, len(headers) - 1)}
        # Add the dictionary to the list
        json_list.append(result)

    return json_list
