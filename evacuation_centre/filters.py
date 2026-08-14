import django_filters

from .models import EvacuationCentre, EvacuationCentreImport


class EvacuationCentreFilter(django_filters.FilterSet):
    country = django_filters.CharFilter(field_name="country", lookup_expr="icontains")
    organization = django_filters.CharFilter(
        field_name="organization", lookup_expr="icontains"
    )
    agency = django_filters.CharFilter(field_name="agency", lookup_expr="icontains")
    province = django_filters.CharFilter(field_name="province", lookup_expr="icontains")
    area_council = django_filters.CharFilter(
        field_name="area_council", lookup_expr="icontains"
    )
    island = django_filters.CharFilter(field_name="island", lookup_expr="icontains")
    village = django_filters.CharFilter(field_name="village", lookup_expr="icontains")
    is_ec_owner_approved = django_filters.BooleanFilter(
        field_name="is_ec_owner_approved"
    )
    is_ec_govt_approved = django_filters.BooleanFilter(field_name="is_ec_govt_approved")
    latitude = django_filters.NumberFilter(method="filter_by_coords")
    longitude = django_filters.NumberFilter(method="filter_by_coords")

    status = django_filters.CharFilter(field_name="status", lookup_expr="iexact")

    class Meta:
        model = EvacuationCentre
        fields = [
            "country",
            "organization",
            "agency",
            "province",
            "area_council",
            "island",
            "village",
            "is_ec_owner_approved",
            "is_ec_govt_approved",
            "latitude",
            "longitude",
            "status",
        ]

    def filter_by_coords(self, queryset, name, value):
        latitude = self.data.get("latitude")
        longitude = self.data.get("longitude")
        if latitude and longitude:
            try:
                lat_val = float(latitude)
                lon_val = float(longitude)
                return queryset.filter(latitude=lat_val, longitude=lon_val)
            except (ValueError, TypeError):
                pass
        if value is not None:
            try:
                val = float(value)
                return queryset.filter(**{name: val})
            except (ValueError, TypeError):
                pass
        return queryset


class EvacuationCentreImportFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name="status", lookup_expr="iexact")
    uploaded_by = django_filters.NumberFilter(field_name="uploaded_by_id")

    class Meta:
        model = EvacuationCentreImport
        fields = ["status", "uploaded_by"]

