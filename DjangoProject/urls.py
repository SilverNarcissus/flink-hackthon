"""
URL configuration for DjangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from DjangoProject.controllers import general_controller
from DjangoProject.controllers import es_controller
from DjangoProject.controllers import job_controller
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # general interface
    path("api/ping", csrf_exempt(general_controller.ping), name="ping"),

    # interface for event stream
    path("api/es/execute_sql", csrf_exempt(es_controller.execute_sql), name="execute_sql"),
    path("api/es/test_query", csrf_exempt(es_controller.test_query), name="test_query"),

    # interface for job management

    # Stop Job (Post)
    path("api/manage/stop/<str:jobId>", csrf_exempt(job_controller.stop), name="stop"),
    
    # Terminate Job (Patch)
    path("api/manage/terminate/<str:jobId>", csrf_exempt(job_controller.terminate), name="terminate"),

    # Get Details of Job in Json
    path("api/manage/job/<str:jobId>", csrf_exempt(job_controller.getDetails), name="getDetails"),

    # Jar management.
    path("api/manage/uploadJar", csrf_exempt(job_controller.uploadJar), name="uploadJar"),
    path("api/manage/runJar/<str:jarId>", csrf_exempt(job_controller.runJar), name="runJar"),
    path("api/manage/planJar/<str:jarId>", csrf_exempt(job_controller.planJar), name="planJar"),
    
    # Get Metrics
    path("api/manage/getMetrics/<str:jobId>", csrf_exempt(job_controller.getMetrics), name="getMetrics"),

    # Get Exceptions
    path("api/manage/getExceptions/<str:jobId>", csrf_exempt(job_controller.getExceptions), name="getExceptions"),

    # Get Config
    path("api/manage/getConfig/<str:jobId>", csrf_exempt(job_controller.getConfig), name="getConfig"),

    # Get Status
    path("api/manage/getStatus/<str:jobId>", csrf_exempt(job_controller.getStatus), name="getStatus"),

    # Get Jobs Overview
    path("api/manage/getJobsOverview", csrf_exempt(job_controller.getJobsOverview), name="getJobsOverview"),
]