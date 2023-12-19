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

# Libraries Imported:
# django.urls: Django module for URL routing.
# healthcare.healthcare_api.views: Importing views from the healthcare_api module.
# rest_framework.authtoken.views: Importing views for the Django REST framework's built-in token authentication.
# rest_framework_simplejwt.views: Importing views for JWT authentication from the djangorestframework_simplejwt library.
# TokenObtainPairView: View for obtaining a pair of refresh and access tokens.
# TokenRefreshView: View for refreshing an access token.
# TokenVerifyView: View for verifying the validity of a token.
# URL Patterns:
# path('', view=views.get_Routes):

# This pattern maps to the root URL and is associated with the get_Routes view function in the healthcare_api.views module.
# path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'):

# This pattern maps to the /token/ URL and is associated with the TokenObtainPairView view, which is responsible for obtaining a pair of refresh and access tokens.
# The name parameter is set to 'token_obtain_pair' for reverse URL lookups.
# path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'):

# This pattern maps to the /token/refresh/ URL and is associated with the TokenRefreshView view, which allows refreshing an access token using a refresh token.
# The name parameter is set to 'token_refresh' for reverse URL lookups.
# path('token/verify/', TokenVerifyView.as_view(), name='token_verify'):

# This pattern maps to the /token/verify/ URL and is associated with the TokenVerifyView view, which verifies the validity of a token.
# The name parameter is set to 'token_verify' for reverse URL lookups.
# path('api-token-auth', view=auth_Token_Views.obtain_auth_token):

# This pattern maps to the /api-token-auth URL and is associated with the obtain_auth_token view from rest_framework.authtoken.views.
# This endpoint is provided by the Django REST framework for obtaining an authentication token.
# JWT Authentication:
# The JWT authentication is set up using the TokenObtainPairView, TokenRefreshView, and TokenVerifyView from the djangorestframework_simplejwt library.
# The TokenObtainPairView is used for obtaining a pair of access and refresh tokens. It requires sending a POST request with valid credentials (usually username and password) to the /token/ endpoint.
# The TokenRefreshView is used for refreshing an access token using a valid refresh token. It requires sending a POST request to the /token/refresh/ endpoint with a valid refresh token.
# The TokenVerifyView is used for verifying the validity of a token. It requires sending a POST request to the /token/verify/ endpoint with a valid access token.
# Conclusion:
# In summary, the provided code sets up URL patterns for a healthcare API, with specific endpoints dedicated to JWT authentication using the djangorestframework_simplejwt library. These endpoints allow users to obtain, refresh, and verify JWT tokens, providing a secure mechanism for authentication in the API. The use of JWT tokens is a common practice in web development to authenticate and authorize users in a stateless and secure manner.

# 1. JSON Web Tokens (JWT):
# Structure: JWTs are strings with three parts separated by dots (.): Header, Payload, and Signature. The three parts are base64-encoded JSON strings.
# Header: Contains information about how the JWT is signed. It typically consists of two parts: the type of the token (JWT) and the signing algorithm being used.

# Payload: Contains the claims. Claims are statements about an entity (typically, the user) and additional data. There are three types of claims: registered, public, and private claims.

# Signature: Used to verify that the sender of the JWT is who it says it is and to ensure that the message wasn't changed along the way.

# Usage:

# Use the TokenObtainPairView to obtain a pair of access and refresh tokens by sending a POST request with valid credentials.
# Use the TokenRefreshView to refresh an access token by sending a POST request with a valid refresh token.
# Use the TokenVerifyView to verify the validity of a token by sending a POST request with a valid access token.
# Customization: Simple JWT provides various configuration options to customize token lifetimes, algorithms, and other settings.

# 3. How Simple JWT Authentication Works:
# Obtaining Tokens:

# When a user logs in or authenticates, the server generates a pair of access and refresh tokens.
# The access token is short-lived and used for authenticating API requests.
# The refresh token is longer-lived and can be used to obtain a new access token when the original access token expires.
# Refreshing Tokens:

# When the access token expires, the client can use the refresh token to obtain a new access token without re-authenticating.
# This helps maintain a balance between security and user convenience.
# Verifying Tokens:

# The server can verify the validity of an access token by checking its signature and expiration time.
# Customization:

# Simple JWT allows customization of token lifetimes, algorithm choices, and other settings based on the application's requirements.
# In summary, Simple JWT authentication provides a straightforward and flexible way to implement JSON Web Token-based authentication in Django REST framework applications. It enhances security by using tokens for authentication and allows for customization to meet specific application needs.
