from rest_framework import filters, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import RoleBasedPermission
from cluster_contact.serializers import FileSerializer
from decmcluster.pagination import CustomPagination

from .models import ClusterContact
from .selectors.cluster_contact_selector import get_cluster_contacts
from .serializers import (
    ClusterContactSerializer,
    SendClusterContactEmailSerializer,
)
from .services.email_service import send_cluster_contact_emails
from .services.import_service import import_contacts_from_docx_file


class ClusterContactListCreateAPIView(ListCreateAPIView):
    queryset = get_cluster_contacts()
    serializer_class = ClusterContactSerializer
    pagination_class = CustomPagination
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["name", "email", "organization"]
    ordering_fields = ["created_at", "updated_at", "name", "organization"]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class ClusterContactDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ClusterContact.objects.all()
    serializer_class = ClusterContactSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), RoleBasedPermission()]


class ClusterContactImportAPIView(APIView):
    """
    Imports contacts from docx file.
    If 'file' is provided in request.FILES, imports from that file;
    otherwise imports from default 'DECM Cluster Mailing List.docx'.
    """

    serializer_class = FileSerializer

    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get("file")
        file_source = uploaded_file.read() if uploaded_file else None

        result = import_contacts_from_docx_file(file_source=file_source)
        return Response(
            {
                "message": "Successfully imported contacts.",
                **result,
            },
            status=status.HTTP_200_OK,
        )


class SendClusterContactEmailAPIView(APIView):
    """
    Sends rich text email to selected or all cluster contacts.
    """

    permission_classes = [IsAuthenticated, RoleBasedPermission]

    def post(self, request, *args, **kwargs):
        serializer = SendClusterContactEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        subject = serializer.validated_data["subject"]
        body = serializer.validated_data["body"]
        emails = serializer.validated_data.get("emails", [])

        result = send_cluster_contact_emails(
            subject=subject,
            body=body,
            emails=emails if emails else None,
        )
        return Response(
            {
                "message": "Emails dispatched successfully.",
                "details": result,
            },
            status=status.HTTP_200_OK,
        )
