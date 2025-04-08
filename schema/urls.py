# schema/urls.py
from django.urls import path
from .views import get_schema

urlpatterns = [
    path('', get_schema, name='get_schema'),  # NOT 'schema/' here, just ''
]