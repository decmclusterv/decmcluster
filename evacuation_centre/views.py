from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import RoleBasedPermission
from decmcluster.pagination import CustomPagination

from .filters import EvacuationCentreFilter, EvacuationCentreImportFilter
from .models import EvacuationCentre, EvacuationCentreImport
from .selectors import get_evacuation_centre_stats
from .serializers import (
    EvacuationCentreImportSerializer,
    EvacuationCentreMinimalSerializer,
    EvacuationCentreSerializer,
    FileImportSerializer,
)
from .services.export_service import generate_evacuation_centre_csv


class EvacuationCentreListCreateAPIView(ListCreateAPIView):
    queryset = EvacuationCentre.objects.all().order_by("id")
    serializer_class = EvacuationCentreSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = EvacuationCentreFilter
    search_fields = ["compound_name", "province", "area_council", "island", "village"]
    permission_classes = [IsAuthenticated, RoleBasedPermission]


class EvacuationCentreDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = EvacuationCentre.objects.all()
    serializer_class = EvacuationCentreSerializer
    permission_classes = [IsAuthenticated, RoleBasedPermission]


class EvacuationCentreImportAPIView(GenericAPIView):
    parser_classes = [MultiPartParser]
    # permission_classes = [IsAuthenticated, RoleBasedPermission]
    serializer_class = FileImportSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        excel_file = serializer.validated_data["file"]
        name = serializer.validated_data["name"]
        uploaded_by = request.user if request.user.is_authenticated else None

        import_request = EvacuationCentreImport.objects.create(
            file=excel_file,
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


class EvacuationCentreStatsAPIView(APIView):
    # permission_classes = [IsAuthenticated, RoleBasedPermission]

    def get(self, request, *args, **kwargs):
        queryset = EvacuationCentre.objects.all()
        filterset = EvacuationCentreFilter(request.GET, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs
        stats_data = get_evacuation_centre_stats(queryset)
        return Response(stats_data, status=status.HTTP_200_OK)


class EvacuationCentreMinimalListAPIView(ListAPIView):
    queryset = (
        EvacuationCentre.objects
        .all()
        .order_by("-created_at")
        .only(
            "id",
            "compound_name",
            "latitude",
            "longitude",
            "is_ec_owner_approved",
            "is_ec_govt_approved",
            "province",
        )
    )
    serializer_class = EvacuationCentreMinimalSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = EvacuationCentreFilter
    search_fields = ["compound_name", "province", "area_council", "island", "village"]


class EvacuationCentreSearchAPIView(ListAPIView):
    """
    GET /api/evacuation-centres/search/?q=<compound_name>
    Returns a minimal list of evacuation centres matching the compound name.
    Designed for autocomplete / lookup use cases.
    """

    serializer_class = EvacuationCentreMinimalSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        q = self.request.query_params.get("search", "").strip()
        qs = (
            EvacuationCentre.objects
            .only(
                "id", "compound_name", "latitude", "longitude",
                "is_ec_owner_approved", "is_ec_govt_approved", "province",
            )
            .order_by("compound_name")
        )
        if q:
            qs = qs.filter(compound_name__icontains=q)
        return qs


class EvacuationCentreExportAPIView(APIView):
    # permission_classes = [IsAuthenticated, RoleBasedPermission]

    def get(self, request, *args, **kwargs):
        queryset = EvacuationCentre.objects.all().order_by("created_at")
        filterset = EvacuationCentreFilter(request.GET, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs

        columns_param = request.GET.get("columns", "")
        requested_columns = None
        if columns_param:
            requested_columns = [
                col.strip() for col in columns_param.split(",") if col.strip()
            ]

        return generate_evacuation_centre_csv(queryset, requested_columns)


class EvacuationCentreImportListAPIView(ListAPIView):
    queryset = (
        EvacuationCentreImport.objects
        .select_related("uploaded_by", "verified_by")
        .all()
        .order_by("-created_at")
    )
    serializer_class = EvacuationCentreImportSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = EvacuationCentreImportFilter
    search_fields = ["file"]
    permission_classes = [IsAuthenticated, RoleBasedPermission]


class EvacuationCentreImportDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = EvacuationCentreImport.objects.select_related(
        "uploaded_by", "verified_by"
    ).all()
    serializer_class = EvacuationCentreImportSerializer
    permission_classes = [IsAuthenticated, RoleBasedPermission]

    def perform_update(self, serializer):
        status_value = self.request.data.get("status")
        if status_value == EvacuationCentreImport.StatusChoices.VERIFIED:
            serializer.save(verified_by=self.request.user)
        else:
            serializer.save()
