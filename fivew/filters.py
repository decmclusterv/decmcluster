from django_filters import rest_framework as filters

from .models import FiveWActivity


class FiveWActivityFilter(filters.FilterSet):
    donor = filters.CharFilter(field_name="donor", lookup_expr="icontains")
    reporting_org_name = filters.CharFilter(
        field_name="reporting_org_name", lookup_expr="icontains"
    )
    state_abyei = filters.CharFilter(field_name="state_abyei", lookup_expr="icontains")
    reporting_month = filters.CharFilter(
        field_name="reporting_month", lookup_expr="iexact"
    )
    activity_status = filters.CharFilter(
        field_name="activity_status", lookup_expr="iexact"
    )
    cluster_name = filters.CharFilter(
        field_name="cluster_name", lookup_expr="icontains"
    )

    status = filters.CharFilter(field_name="status", lookup_expr="iexact")

    class Meta:
        model = FiveWActivity
        fields = [
            "donor",
            "reporting_org_name",
            "state_abyei",
            "reporting_month",
            "activity_status",
            "cluster_name",
            "status",
        ]
