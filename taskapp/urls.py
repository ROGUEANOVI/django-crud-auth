from django.urls import path
from taskapp  import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', views.home, name='home'),
    path('signup/',  views.signUp, name='signup'),
    path('signin/', views.signIn, name='signin'),
    path('signout/', views.signOut, name='signout'),
    path('tasks/', login_required(views.listTasks) , name='tasks'),
    path('tasks/completed', login_required(views.listCompletedTasks) , name='completed_tasks'),
    path('tasks/create', login_required(views.createTask), name='create_task'),
    path('tasks/edit/<int:id>', login_required(views.editTask), name='edit_task'),
    path('tasks/complete/<int:id>', login_required(views.completeTask), name='complete_task'),
    path('tasks/details-task/<int:id>', login_required(views.detailsTask), name='details_task'),
    path('tasks/delete/<int:id>', login_required(views.deleteTask), name='delete_task'),
]