from django.urls import path
from account import views

urlpatterns = [
    path('',views.UserView.as_view()),
]
