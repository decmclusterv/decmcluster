from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import RoleBasedPermission
from decmcluster.pagination import CustomPagination

from .filters import NewsletterFilter
from .models import Newsletter
from .selectors.newsletter_selector import get_newsletter_subscribers
from .serializers import (
    NewsletterSerializer,
    SendNewsletterEmailSerializer,
    NewsletterSubscriptionUpdateSerializer,
)
from .services.newsletter_service import (
    send_custom_newsletter_emails,
    update_subscription_status,
)


class NewsletterListCreateAPIView(ListCreateAPIView):
    queryset = get_newsletter_subscribers()
    serializer_class = NewsletterSerializer
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = NewsletterFilter
    search_fields = ["email"]
    ordering_fields = ["created_at", "email"]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class NewsletterDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer

    def get_permissions(self):
        return [IsAuthenticated(), RoleBasedPermission()]


class SendNewsletterEmailAPIView(APIView):
    permission_classes = [IsAuthenticated, RoleBasedPermission]

    def post(self, request, *args, **kwargs):
        serializer = SendNewsletterEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        subject = serializer.validated_data["subject"]
        body = serializer.validated_data["body"]
        emails = serializer.validated_data.get("emails", [])

        # If no emails are specified, pass None to send to all active subscribers
        result = send_custom_newsletter_emails(subject, body, emails=emails if emails else None)
        return Response(
            {
                "message": "Newsletter emails dispatched successfully.",
                "details": result,
            },
            status=status.HTTP_200_OK,
        )


class NewsletterUnsubscribeAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = NewsletterSubscriptionUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        is_subscribed = serializer.validated_data["is_subscribed"]

        newsletter = update_subscription_status(email, is_subscribed)
        message = "Unsubscribed from newsletter successfully." if not is_subscribed else "Subscribed to newsletter successfully."
        return Response(
            {
                "message": message,
                "data": NewsletterSerializer(newsletter).data,
            },
            status=status.HTTP_200_OK,
        )



