from django.urls import path
from . import views

urlpatterns = [
    path("login_user", views.login_user, name="login"),
    path("logout_user", views.logout_user, name="logout"),
    path("create_user", views.create_user, name="create_user"),
]