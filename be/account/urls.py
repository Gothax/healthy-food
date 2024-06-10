from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import api

# config path('api/', include('account.urls')),
urlpatterns = [
    path('me/', api.me, name='me'),
    path('signup/', api.signup, name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('editprofile/', api.editprofile, name='editprofile'),
    path('editpassword/', api.editpassword, name='editpassword'),
    
    path('follow/<uuid:pk>/request/', api.send_follow, name='send_follow'),
    path('follow/<uuid:pk>/status/', api.check_follow, name='check_follow'),
    
    path('seller/register/', api.register_seller, name='register_seller'),
    path('me/noimg/', api.me_noimg, name='me_noimg'),
]

