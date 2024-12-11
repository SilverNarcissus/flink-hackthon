import json
import requests
from django.http import JsonResponse
from business_logic import es_business_logic


def execute_sql(request):
    if request.method == 'POST':
        try:
            # Step 1: Get the SQL from the POST request JSON body
            data = json.loads(request.body)
            sql_query = data.get('sql')

            if not sql_query:
                return JsonResponse({'error': 'No SQL query provided'}, status=400)

            print(sql_query)

            # Submit job to flink cluster and get result
            output = es_business_logic.submit_job(sql_query)

            job_id = es_business_logic.extract_job_id(output)

            if not job_id:
                return JsonResponse({'error': output}, status=400)

            # Step 5: Return the job ID as the response
            return JsonResponse({'job_id': job_id})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def test_query(request):
    if request.method == 'POST':
        try:
            # Step 1: Get the SQL from the POST request JSON body
            data = json.loads(request.body)
            sql_query = data.get('sql')

            if not sql_query:
                return JsonResponse({'error': 'No SQL query provided'}, status=400)

            # Submit job to flink cluster and get result
            output = es_business_logic.submit_job(sql_query)

            result = es_business_logic.table_to_json(output)

            # Step 5: Return the job ID as the response
            return JsonResponse({'result': result})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def get_job_overview(request, job_id):
    if request.method == 'GET':
        try:
            response = requests.get('https://api.ipify.org?format=json')
            response.raise_for_status()
            ip_data = response.json()
            port = 8081

            # Step 5: Return the job ID as the response
            return JsonResponse({'url': "http://{0}:{1}/#/job/running/{2}/overview".format(ip_data['ip'], port, job_id)})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)