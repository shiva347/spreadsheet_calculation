from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegisterAPIView.as_view(), name='register'),
    path('login/', views.UserLogIn.as_view(), name='login'),
]
