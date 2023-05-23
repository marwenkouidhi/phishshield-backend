
from django.urls import path, include
from .views import classfiyEmail, EmailView, fetchEmails
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('checkEmail', classfiyEmail),
    path('fetchemails', fetchEmails),
    path('', EmailView.as_view())

]
