from django.urls import path

from .views import (
    NewsletterDetailAPIView,
    NewsletterListCreateAPIView,
    SendNewsletterEmailAPIView,
    NewsletterUnsubscribeAPIView,
)

urlpatterns = [
    path(
        "newsletter/",
        NewsletterListCreateAPIView.as_view(),
        name="newsletter-list-create",
    ),
    path(
        "newsletter/<int:pk>/",
        NewsletterDetailAPIView.as_view(),
        name="newsletter-detail",
    ),
    path(
        "newsletter/send-email/",
        SendNewsletterEmailAPIView.as_view(),
        name="newsletter-send-email",
    ),
    path(
        "newsletter/unsubscribe/",
        NewsletterUnsubscribeAPIView.as_view(),
        name="newsletter-unsubscribe",
    ),
]
