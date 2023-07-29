from django.urls import path
from .views import TaskReorder, RegisterPage, Login, TaskList, TaskDetail, TaskCreate, TaskDeleteView, TaskUpdate
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', TaskDeleteView.as_view(), name='task-delete'),

    path('register/', RegisterPage.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('task-reorder/', TaskReorder.as_view(), name='task-reorder'),
]

