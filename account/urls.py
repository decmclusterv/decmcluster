from django.urls import path

from .views import (
    ChangePasswordAPIView,
    ResendVerificationEmailAPIView,
    SuperAdminUserDetailAPIView,
    SuperAdminUserListAPIView,
    SuperAdminUserVerifyAPIView,
    UserEmailVerificationAPIView,
    UserLoginAPIView,
    UserRegistrationAPIView,
)

urlpatterns = [
    path("register/", UserRegistrationAPIView.as_view(), name="register"),
    path("login/", UserLoginAPIView.as_view(), name="login"),
    path("change-password/", ChangePasswordAPIView.as_view(), name="change-password"),
    path("verify-email/", UserEmailVerificationAPIView.as_view(), name="verify-email"),
    path(
        "resend-verification/",
        ResendVerificationEmailAPIView.as_view(),
        name="resend-verification",
    ),
    path(
        "verify/<int:pk>/",
        SuperAdminUserVerifyAPIView.as_view(),
        name="superuser-verify",
    ),
    path("users/", SuperAdminUserListAPIView.as_view(), name="superuser-user-list"),
    path(
        "users/<int:pk>/",
        SuperAdminUserDetailAPIView.as_view(),
        name="superuser-user-detail",
    ),
]
