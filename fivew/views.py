from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as rest_filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

from decmcluster.pagination import CustomPagination

from .filters import FiveWActivityFilter
from .models import FiveWActivity, FiveWImport
from .serializers import FiveWActivitySerializer, FiveWImportSerializer
from .services.export_service import generate_fivew_csv


from rest_framework.response import Response
from rest_framework import status


class FiveWActivityListCreateAPIView(ListCreateAPIView):
    serializer_class = FiveWActivitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    pagination_class = CustomPagination

    filterset_class = FiveWActivityFilter
    search_fields = [
        "donor",
        "reporting_org_name",
        "activity",
        "indicator",
        "state_abyei",
        "cluster_name",
    ]
    def get_queryset(self):
        queryset = FiveWActivity.objects.all().order_by("-created_at")
        status_param = self.request.query_params.get("status")
        if status_param:
            return queryset
        return queryset.filter(status=FiveWActivity.StatusChoices.VERIFIED)

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(uploaded_by=self.request.user)
        else:
            serializer.save()

class FiveWActivityRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = FiveWActivitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return FiveWActivity.objects.all()

    def perform_update(self, serializer):
        status_value = self.request.data.get("status")
        if status_value == FiveWActivity.StatusChoices.VERIFIED:
            serializer.save(verified_by=self.request.user)
        else:
            serializer.save()


class FiveWImportListCreateAPIView(ListCreateAPIView):
    queryset = (
        FiveWImport.objects
        .all()
        .select_related("uploaded_by", "verified_by")
        .order_by("-created_at")
    )
    serializer_class = FiveWImportSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        # Automatically set the uploaded_by field to the current user if authenticated
        if self.request.user.is_authenticated:
            serializer.save(uploaded_by=self.request.user)
        else:
            serializer.save()


class FiveWImportRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = FiveWImport.objects.all().select_related("uploaded_by", "verified_by")
    serializer_class = FiveWImportSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class FiveWActivityExportAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        status_param = request.GET.get("status")
        if status_param:
            queryset = FiveWActivity.objects.all().order_by("created_at")
        else:
            queryset = FiveWActivity.objects.filter(
                status=FiveWActivity.StatusChoices.VERIFIED
            ).order_by("created_at")
        filterset = FiveWActivityFilter(request.GET, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs

        columns_param = request.GET.get("columns", "")
        requested_columns = None
        if columns_param:
            requested_columns = [
                col.strip() for col in columns_param.split(",") if col.strip()
            ]

        return generate_fivew_csv(queryset, requested_columns)


from rest_framework.permissions import IsAuthenticated


class FiveWActivityReverifyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        try:
            instance = FiveWActivity.objects.get(pk=pk)
        except FiveWActivity.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if instance.uploaded_by != request.user:
            return Response(
                {"detail": "Only the uploader can resubmit for verification."},
                status=status.HTTP_403_FORBIDDEN,
            )

        instance.status = FiveWActivity.StatusChoices.UNVERIFIED
        instance.verified_by = None
        instance.save()

        serializer = FiveWActivitySerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
