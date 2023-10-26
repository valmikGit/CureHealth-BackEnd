from django.urls import path
from healthcare.healthcare_api import views
from healthcare.healthcare_api.views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView
)

urlpatterns = [
    path('', view=views.get_Routes),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('notes/', view=views.get_Notes)
]

