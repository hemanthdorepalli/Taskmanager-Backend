from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('tasks/', views.task_list_create, name='task_list_create'),
    path('tasks/<int:pk>/', views.task_detail_update_delete, name='task_detail_update_delete'),
]
