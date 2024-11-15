from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin URL
    path('api/', include('tasks.urls')),  # API routes for tasks, registration, and login
]
