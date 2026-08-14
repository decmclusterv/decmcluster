import django_filters

from .models import Displacement, DisplacementImport


class DisplacementFilter(django_filters.FilterSet):
    operation = django_filters.CharFilter(
        field_name="operation", lookup_expr="icontains"
    )
    admin0_name = django_filters.CharFilter(
        field_name="admin0_name", lookup_expr="icontains"
    )
    admin1_name = django_filters.CharFilter(
        field_name="admin1_name", lookup_expr="icontains"
    )
    admin2_name = django_filters.CharFilter(
        field_name="admin2_name", lookup_expr="icontains"
    )
    displacement_reason = django_filters.CharFilter(
        field_name="displacement_reason", lookup_expr="icontains"
    )
    operation_status = django_filters.CharFilter(
        field_name="operation_status", lookup_expr="iexact"
    )
    reporting_year = django_filters.NumberFilter(field_name="reporting_year")
    reporting_month = django_filters.NumberFilter(field_name="reporting_month")
    status = django_filters.CharFilter(field_name="status", lookup_expr="iexact")

    class Meta:
        model = Displacement
        fields = [
            "operation",
            "admin0_name",
            "admin1_name",
            "admin2_name",
            "displacement_reason",
            "operation_status",
            "reporting_year",
            "reporting_month",
            "status",
        ]


class DisplacementImportFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name="status", lookup_expr="iexact")
    uploaded_by = django_filters.NumberFilter(field_name="uploaded_by_id")

    class Meta:
        model = DisplacementImport
        fields = ["status", "uploaded_by"]

