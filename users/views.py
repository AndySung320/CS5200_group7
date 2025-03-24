from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import RegisterSerializer
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

@api_view(['POST'])
def register_user(request):
    """
    This endpoint allows a new user to register by providing required fields:
    - email
    - name
    - password
    - verify_password
    - role (optional, defaults to 'Student' if not provided)

    Steps:
    1. Initialize the RegisterSerializer with incoming request data.
    2. Validate the data using the serializer.
       - If invalid (e.g., passwords don't match, email already exists), return HTTP 400 with error messages.
    3. If valid, save the new user to the database.
    4. Return a success message with HTTP status 201 (Created).

    Parameters:
        request (Request): The incoming HTTP POST request containing user registration data.

    Returns:
        Response:
            - 201 CREATED with success message if registration succeeds.
            - 400 BAD REQUEST with validation errors if registration fails.
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for obtaining JWT access and refresh tokens.

    This view uses the CustomTokenObtainPairSerializer to:
    - Authenticate users using email and password.
    - Return both access and refresh tokens.
    - Include additional user information in the response and token payload, such as:
        - user_id
        - name
        - role

    Endpoint: POST /api/token/
    Request Body:
        {
            "email": "user@example.com",
            "password": "your_password"
        }

    Successful Response:
        {
            "refresh": "<refresh_token>",
            "access": "<access_token>",
            "user_id": 1,
            "name": "Thomas",
            "role": "Student"
        }

    This enhanced response allows frontend applications to retrieve key user info
    without needing to decode the JWT manually.
    """
    serializer_class = CustomTokenObtainPairSerializer

class LogoutView(APIView):
    """
    Allows authenticated users to log out by blacklisting their refresh token.

    Steps:
    1. Requires the user to be authenticated (access token in header).
    2. Accepts a refresh token in the POST body.
    3. Attempts to blacklist the given refresh token.
       - If successful, returns HTTP 205 (Reset Content).
       - If the token is invalid or missing, returns HTTP 400.

    Endpoint: POST /api/logout/
    Request data: { "refresh": "<refresh_token>" }
    Response: { "message": "Logout successful." }

    Notes:
    - Requires `rest_framework_simplejwt.token_blacklist` app to be enabled.
    - Only refresh tokens can be blacklisted (not access tokens).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)