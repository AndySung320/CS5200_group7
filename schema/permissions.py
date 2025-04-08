from rest_framework.permissions import BasePermission

class IsAdminOrInstructor(BasePermission):
    """
    Custom permission to allow only Admins or Instructors to access a view.
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and (
                request.user.is_superuser or
                request.user.role in ['Admin', 'Instructor']
            )
        )