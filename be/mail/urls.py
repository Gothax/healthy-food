from django.urls import path
from .views import SendMailAPIView

urlpatterns = [
    path('', SendMailAPIView.as_view(), name='mail_send'),
]
