from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from schema.permissions import IsAdminOrInstructor 
from users.models import User
from sql_app.models import SQLProblem, Attempt

@api_view(['GET'])
# @permission_classes([IsAdminOrInstructor])  
def get_schema(request):

    users = User.objects.all().values('user_id', 'name')
    problems = SQLProblem.objects.all().values('problem_id', 'title', 'difficulty_level', 'topic_id')
    attempts = Attempt.objects.all().values(
        'attempt_id', 'user_id', 'problem_id', 'score',
        'status', 'submission_date', 'time_taken', 'hints_used'
    )

    return Response({
        "users": list(users),
        "problems": list(problems),
        "attempts": list(attempts)
    })