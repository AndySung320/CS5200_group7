from django.urls import path
from .views import problem_list, problem_detail, AttemptSubmitView

urlpatterns = [
    path('sql-problems/', problem_list, name='problem_list'),
    path('problems/<int:problem_id>/', problem_detail, name='problem_detail'),
    path('problems/<int:problem_id>/attempt/', AttemptSubmitView.as_view(), name='attempt_submit'),
]