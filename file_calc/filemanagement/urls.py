from django.urls import path
from . import views

urlpatterns = [
    path('compute/', views.FileUploadView.as_view(), name='register'),
]