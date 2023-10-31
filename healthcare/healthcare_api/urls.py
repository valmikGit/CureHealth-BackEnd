from django.urls import path
from healthcare.healthcare_api import views
from rest_framework.authtoken import views as auth_Token_Views
# from healthcare.healthcare_api.views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
    TokenVerifyView
)

urlpatterns = [
    path('', view=views.get_Routes),
    # path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api-token-auth', view=auth_Token_Views.obtain_auth_token),
    # path('notes/', view=views.get_Notes),
]

