from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import RoleBasedPermission
from decmcluster.pagination import CustomPagination

from .filters import DisplacementFilter, DisplacementImportFilter
from .models import Displacement, DisplacementImport
from .selectors import get_displacement_stats, get_displacement_unique_filters
from .serializers import (
    DisplacementImportSerializer,
    DisplacementSerializer,
    FileImportSerializer,
)
from .services.export_service import generate_displacement_csv
from .utils import send_displacement_verification_email


class DisplacementListCreateAPIView(ListCreateAPIView):
    serializer_class = DisplacementSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = DisplacementFilter
    search_fields = ["operation", "admin1_name", "admin2_name", "displacement_reason"]
    # permission_classes = [IsAuthenticated, RoleBasedPermission]

    def get_queryset(self):
        queryset = Displacement.objects.all().order_by("id")
        status_param = self.request.query_params.get("status")
        if status_param:
            return queryset
        return queryset.filter(status=Displacement.StatusChoices.VERIFIED)

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


class DisplacementDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = DisplacementSerializer
    permission_classes = [IsAuthenticated, RoleBasedPermission]

    def get_queryset(self):
        return Displacement.objects.all()

    def perform_update(self, serializer):
        status_value = self.request.data.get("status")
        if status_value == Displacement.StatusChoices.VERIFIED:
            serializer.save(verified_by=self.request.user)
        else:
            serializer.save()


class DisplacementImportAPIView(GenericAPIView):
    parser_classes = [MultiPartParser]
    # permission_classes = [IsAuthenticated, RoleBasedPermission]
    serializer_class = FileImportSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        uploaded_file = serializer.validated_data["file"]
        name = serializer.validated_data.get("name", "")
        uploaded_by = request.user if request.user.is_authenticated else None

        import_request = DisplacementImport.objects.create(
            file=uploaded_file,
            uploaded_by=uploaded_by,
            name=name,
        )

        return Response(
            {
                "message": "File uploaded successfully. It will be processed after admin verification.",
                "id": import_request.id,
            },
            status=status.HTTP_201_CREATED,
        )


class DisplacementStatsAPIView(APIView):
    # permission_classes = [IsAuthenticated, RoleBasedPermission]

    def get(self, request, *args, **kwargs):
        queryset = Displacement.objects.filter(status=Displacement.StatusChoices.VERIFIED)

        filterset = DisplacementFilter(request.GET, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs
        stats_data = get_displacement_stats(queryset)
        return Response(stats_data, status=status.HTTP_200_OK)


class DisplacementExportAPIView(APIView):
    # permission_classes = [IsAuthenticated, RoleBasedPermission]

    def get(self, request, *args, **kwargs):
        queryset = Displacement.objects.filter(
            status=Displacement.StatusChoices.VERIFIED
        ).order_by("-reporting_date")

        filterset = DisplacementFilter(request.GET, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs

        columns_param = request.GET.get("columns", "")
        requested_columns = None
        if columns_param:
            requested_columns = [
                col.strip() for col in columns_param.split(",") if col.strip()
            ]

        return generate_displacement_csv(queryset, requested_columns)


class DisplacementUniqueFiltersAPIView(APIView):
    # permission_classes = [IsAuthenticated, RoleBasedPermission]

    def get(self, request, *args, **kwargs):
        data = get_displacement_unique_filters()
        return Response(data, status=status.HTTP_200_OK)


class DisplacementImportListAPIView(ListAPIView):
    queryset = (
        DisplacementImport.objects
        .select_related("uploaded_by", "verified_by")
        .all()
        .order_by("-created_at")
    )
    serializer_class = DisplacementImportSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = DisplacementImportFilter
    search_fields = ["file"]
    permission_classes = [IsAuthenticated, RoleBasedPermission]


class DisplacementImportDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = (
        DisplacementImport.objects
        .select_related("uploaded_by", "verified_by")
        .all()
    )
    serializer_class = DisplacementImportSerializer
    permission_classes = [IsAuthenticated, RoleBasedPermission]

    def perform_update(self, serializer):
        status_value = self.request.data.get("status")
        if status_value == DisplacementImport.StatusChoices.VERIFIED:
            serializer.save(verified_by=self.request.user)
        else:
            serializer.save()


class DisplacementReverifyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        try:
            instance = Displacement.objects.get(pk=pk)
        except Displacement.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if instance.uploaded_by != request.user:
            return Response(
                {"detail": "Only the uploader can resubmit for verification."},
                status=status.HTTP_403_FORBIDDEN,
            )

        instance.status = Displacement.StatusChoices.UNVERIFIED
        instance.verified_by = None
        instance.save()

        comment_value = request.data.get("comment")
        # Resend email to admin
        send_displacement_verification_email(instance, comment=comment_value)

        serializer = DisplacementSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

