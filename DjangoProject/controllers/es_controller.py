from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def execute_sql(request):
    return HttpResponse(request)