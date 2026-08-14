from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as rest_filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

from decmcluster.pagination import CustomPagination

from .filters import VillageAssessmentFilter
from .models import VillageAssessment, VillageAssessmentImport
from .serializers import VillageAssessmentImportSerializer, VillageAssessmentSerializer
from .services.export_service import generate_village_assessment_csv


from rest_framework.response import Response
from rest_framework import status


class VillageAssessmentListCreateAPIView(ListCreateAPIView):
    serializer_class = VillageAssessmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    filterset_class = VillageAssessmentFilter
    pagination_class = CustomPagination

    search_fields = [
        "province",
        "area_council",
        "village_name",
        "village_other",
        "validation_status",
    ]
    ordering_fields = ["assessment_date", "idp_individuals_total", "created_at"]

    def get_queryset(self):
        queryset = VillageAssessment.objects.all().order_by("-assessment_date", "-created_at")
        status_param = self.request.query_params.get("status")
        if status_param:
            return queryset
        return queryset.filter(status=VillageAssessment.StatusChoices.VERIFIED)

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(uploaded_by=self.request.user)
        else:
            serializer.save()

class VillageAssessmentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = VillageAssessmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return VillageAssessment.objects.all()

    def perform_update(self, serializer):
        status_value = self.request.data.get("status")
        if status_value == VillageAssessment.StatusChoices.VERIFIED:
            serializer.save(verified_by=self.request.user)
        else:
            serializer.save()


class VillageAssessmentImportListCreateAPIView(ListCreateAPIView):
    queryset = (
        VillageAssessmentImport.objects
        .all()
        .select_related("uploaded_by", "verified_by")
        .order_by("-created_at")
    )
    serializer_class = VillageAssessmentImportSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(uploaded_by=self.request.user)
        else:
            serializer.save()


class VillageAssessmentImportRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = VillageAssessmentImport.objects.all().select_related(
        "uploaded_by", "verified_by"
    )
    serializer_class = VillageAssessmentImportSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class VillageAssessmentExportAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        status_param = request.GET.get("status")
        if status_param:
            queryset = VillageAssessment.objects.all().order_by("created_at")
        else:
            queryset = VillageAssessment.objects.filter(
                status=VillageAssessment.StatusChoices.VERIFIED
            ).order_by("created_at")
        filterset = VillageAssessmentFilter(request.GET, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs

        columns_param = request.GET.get("columns", "")
        requested_columns = None
        if columns_param:
            requested_columns = [
                col.strip() for col in columns_param.split(",") if col.strip()
            ]

        return generate_village_assessment_csv(queryset, requested_columns)


from rest_framework.permissions import IsAuthenticated


class VillageAssessmentReverifyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        try:
            instance = VillageAssessment.objects.get(pk=pk)
        except VillageAssessment.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if instance.uploaded_by != request.user:
            return Response(
                {"detail": "Only the uploader can resubmit for verification."},
                status=status.HTTP_403_FORBIDDEN,
            )

        instance.status = VillageAssessment.StatusChoices.UNVERIFIED
        instance.verified_by = None
        instance.save()

        serializer = VillageAssessmentSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
