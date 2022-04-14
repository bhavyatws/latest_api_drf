from django.urls import path
from account.views import UserView

urlpatterns = [
    path('',UserView.as_view()),
]
