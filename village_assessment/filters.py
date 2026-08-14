from django_filters import rest_framework as filters

from .models import VillageAssessment


class VillageAssessmentFilter(filters.FilterSet):
    province = filters.CharFilter(field_name="province", lookup_expr="icontains")
    area_council = filters.CharFilter(
        field_name="area_council", lookup_expr="icontains"
    )
    village_name = filters.CharFilter(
        field_name="village_name", lookup_expr="icontains"
    )
    validation_status = filters.CharFilter(
        field_name="validation_status", lookup_expr="iexact"
    )
    idp_present = filters.BooleanFilter(field_name="idp_present")
    returnees_present = filters.BooleanFilter(field_name="returnees_present")
    assessment_date_start = filters.DateFilter(
        field_name="assessment_date", lookup_expr="gte"
    )
    assessment_date_end = filters.DateFilter(
        field_name="assessment_date", lookup_expr="lte"
    )

    status = filters.CharFilter(field_name="status", lookup_expr="iexact")

    class Meta:
        model = VillageAssessment
        fields = [
            "province",
            "area_council",
            "village_name",
            "validation_status",
            "idp_present",
            "returnees_present",
            "status",
        ]
