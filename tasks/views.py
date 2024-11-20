from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny  # To enforce authentication
from .models import Task
from .serializers import RegistrationSerializer, TaskSerializer  # Import the necessary serializers


# Registration View (public access)
@api_view(['POST'])
@permission_classes([AllowAny])  # Allow any user to register (no authentication needed)
def register(request):
    """
    Registers a new user with username, email, and password.
    """
    serializer = RegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()  # Save the new user
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login View (public access, token-based login)
@api_view(['POST'])
@permission_classes([AllowAny])  # Allow any user to log in (no authentication needed)
def login(request):
    """
    Authenticate the user and provide a JWT token.
    """
    username = request.data.get("username")
    password = request.data.get("password")

    # Check if username and password are provided
    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    # Authenticate user
    user = authenticate(username=username, password=password)
    
    # If the user is authenticated, generate JWT token
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({'access_token': str(refresh.access_token)}, status=status.HTTP_200_OK)
    
    # If the credentials are invalid, return an error
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


# Task List and Creation (only authenticated users can view and create tasks)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])  # Ensure only authenticated users can access this view
def task_list_create(request):
    """
    Retrieve all tasks belonging to the current authenticated user (GET)
    or create a new task (POST) for the authenticated user.
    """

    if request.method == 'GET':
        tasks = Task.objects.filter(user=request.user)
        
        if tasks.exists():
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({'message': 'No tasks found'}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        
        if serializer.is_valid():
            # Associate the task with the logged-in user
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Task Detail, Update, and Delete (only the task owner can access, update, or delete the task)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])  # Ensure only authenticated users can access this view
def task_detail_update_delete(request, pk):
    """
    Retrieve, update or delete a specific task for the authenticated user.
    """
    try:
        # Check if the task exists and belongs to the authenticated user
        task = Task.objects.get(pk=pk, user=request.user)
    except Task.DoesNotExist:
        return Response({'message': 'Task not found or you do not have permission to access it'},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
