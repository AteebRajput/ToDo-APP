from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate , TaskUpdate , TaskDelete,RegisterPage
from . import views
urlpatterns = [
    path("",TaskList.as_view(),name='tasklist'),
    path("login",views.login_user,name='login'),
    path("logout",views.logout_user,name='logout'),
    path("register",RegisterPage.as_view(),name='register'),
    path("task/<int:pk>/",TaskDetail.as_view(),name='taskdetail'),
    path("task-update/<int:pk>/",TaskUpdate.as_view(),name='task-update'),
    path("task-delete/<int:pk>/",TaskDelete.as_view(),name='task-delete'),
    path("task-create",TaskCreate.as_view(),name='task-create'),
    
]
