from django.urls import path, include
from .views import LoginView, LogView

urlpatterns = [

    path('login/', LoginView.as_view()),
    path('log', LogView.as_view()),
]
