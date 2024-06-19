from django.urls import path
from .views import ChatWithGpt,get_faq_data

urlpatterns = [
    path('', ChatWithGpt.as_view(), name='chat_with_gpt'),
    path('faq/', get_faq_data, name='get_faq_data'),
]
