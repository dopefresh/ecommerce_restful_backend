from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from accounts.views import (
    SignUpUserView, 
    SignUpEmployeeView
)

app_name = 'accounts'

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/employee/', SignUpEmployeeView.as_view(), name='signup-employee'),
    path('signup/user/', SignUpUserView.as_view(), name='signup-user'),
]
