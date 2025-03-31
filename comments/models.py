from django.db import models
from django.conf import settings

class Comment(models.Model):
    # If you have a Problem model in another app (e.g., problems app):
    # from problems.models import Problem
    # problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='comments')
    
    # OR, if you don't have a Problem model, simply store an integer:
    problem_id = models.IntegerField()  # Stores the ID of the problem
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Comment"
        managed = False

    def __str__(self):
        return f"Comment by {self.user.username} on Problem {self.problem_id}"