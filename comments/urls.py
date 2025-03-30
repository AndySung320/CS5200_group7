from django.urls import path
from .views import CommentListView, CommentAddView

urlpatterns = [
    # List all comments for a problem:
    path('<int:problem_id>/', CommentListView.as_view(), name='comment-list'),
    # Add a comment to a problem:
    path('<int:problem_id>/add/', CommentAddView.as_view(), name='comment-add'),
]