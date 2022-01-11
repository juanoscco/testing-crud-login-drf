from django.urls import path
from user import views

app_name = "user"

urlpatterns = [
    path("register/", views.CreateUserView.as_view(), name="register"),
    path("login/", views.CreateTokenView.as_view(), name="login"),
    path("me/", views.ManagerUserView.as_view(), name="me"),
    path("logout/", views.Logout.as_view(), name="logout"),
]