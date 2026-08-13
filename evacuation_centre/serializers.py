from rest_framework import serializers

from .models import EvacuationCentre, EvacuationCentreImport
from .services.import_service import find_duplicate_compound_names


class EvacuationCentreSerializer(serializers.ModelSerializer):
    # Fields that are nullable in DB (to preserve existing data) but
    # required on new submissions via the API.
    island = serializers.CharField(required=True)
    village = serializers.CharField(required=True)
    primary_contact = serializers.CharField(required=True)
    secondary_contact = serializers.CharField(required=True)
    compound_function = serializers.CharField(required=True)
    name_of_outside_temporary_shelter = serializers.CharField(required=True)
    outside_temporary_shelter_capacity = serializers.IntegerField(required=True)
    electricity_source = serializers.CharField(required=True)
    drinking_water_source = serializers.CharField(required=True)
    washing_water_source = serializers.CharField(required=True)
    water_storage_capacity_litres = serializers.IntegerField(required=True)
    no_of_buildings = serializers.IntegerField(required=True)
    no_of_rooms = serializers.IntegerField(required=True)
    internal_building_evacuee_capacity = serializers.IntegerField(required=True)
    disaster_suitable_for = serializers.CharField(required=True)
    enginerring_certified_cyclone_rating = serializers.CharField(required=True)
    total_mens_toilet = serializers.IntegerField(required=True)
    total_womens_toilet = serializers.IntegerField(required=True)
    total_unisex_toilet = serializers.IntegerField(required=True)
    total_disability_access_toilet = serializers.IntegerField(required=True)
    total_mens_shower = serializers.IntegerField(required=True)
    total_womens_shower = serializers.IntegerField(required=True)
    total_unisex_shower = serializers.IntegerField(required=True)
    total_disability_access_shower = serializers.IntegerField(required=True)
    communication_back_up = serializers.CharField(required=True)

    class Meta:
        model = EvacuationCentre
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_compound_name(self, value):
        if not value:
            return value
        clean_name = str(value).strip()
        qs = EvacuationCentre.objects.filter(compound_name__iexact=clean_name)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "Duplicate data: An evacuation centre with this compound name already exists."
            )
        return clean_name


from .services.import_service import (
    find_duplicate_compound_names,
    find_missing_required_fields,
)


class FileImportSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_blank=True)
    file = serializers.FileField()

    def validate_file(self, value):
        file_name = value.name.lower()
        if not file_name.endswith((".xlsx", ".xls", ".csv")):
            raise serializers.ValidationError(
                "Only Excel (.xlsx, .xls) or CSV (.csv) files are allowed."
            )

        # Check for missing required fields
        missing_errors = find_missing_required_fields(value)
        if missing_errors:
            # Return top 5 missing field errors for readability
            error_str = " | ".join(missing_errors[:5])
            if len(missing_errors) > 5:
                error_str += f" and {len(missing_errors) - 5} more errors"
            raise serializers.ValidationError(
                f"File validation failed due to missing required fields: {error_str}"
            )

        duplicates = find_duplicate_compound_names(value)
        if duplicates:
            duplicate_str = ", ".join(sorted(duplicates)[:5])
            if len(duplicates) > 5:
                duplicate_str += f" and {len(duplicates) - 5} more"
            raise serializers.ValidationError(
                f"Duplicate data: The uploaded file contains compound name(s) that already exist or appear multiple times: {duplicate_str}."
            )
        return value



class EvacuationCentreMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvacuationCentre
        fields = [
            "id",
            "compound_name",
            "latitude",
            "longitude",
            "is_ec_owner_approved",
            "is_ec_govt_approved",
            "province",
        ]
        read_only_fields = fields


class EvacuationCentreImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvacuationCentreImport
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "verified_by"]
