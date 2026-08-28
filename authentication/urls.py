from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from authentication.views import LoginView

urlpatterns=[
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),
]
