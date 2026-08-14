from rest_framework import serializers

from .models import FiveWActivity, FiveWImport
from .services.import_service import find_missing_required_fields


from displacement.serializers import UserMinSerializer


class FiveWActivitySerializer(serializers.ModelSerializer):
    # Enforce API validation required rules for all fields
    donor = serializers.CharField(required=True)
    donor_names = serializers.CharField(required=True)
    reporting_org_name = serializers.CharField(required=True)
    ro_code = serializers.CharField(required=True)
    reporting_org_type = serializers.CharField(required=True)
    other_ip_name = serializers.CharField(required=True)
    ip_code = serializers.CharField(required=True)
    ip_type = serializers.CharField(required=True)
    reporting_month = serializers.CharField(required=True)
    activity_status = serializers.CharField(required=True)
    state_abyei = serializers.CharField(required=True)
    admin1_code = serializers.CharField(required=True)
    province = serializers.CharField(required=True)
    admin2_code = serializers.CharField(required=True)
    location_evac_name = serializers.CharField(required=True)
    cluster_name = serializers.CharField(required=True)
    hrp_non_hrp = serializers.CharField(required=True)
    project_number = serializers.CharField(required=True)
    project_name = serializers.CharField(required=True)
    activity = serializers.CharField(required=True)
    indicator = serializers.CharField(required=True)
    unit = serializers.CharField(required=True)
    target = serializers.IntegerField(required=True)
    total_value = serializers.DecimalField(
        max_digits=20, decimal_places=4, required=True
    )
    new_beneficiaries = serializers.BooleanField(required=True)
    beneficiaries_type_under_18 = serializers.CharField(required=True)
    child_male_under_18 = serializers.IntegerField(required=True)
    child_female_under_18 = serializers.IntegerField(required=True)
    adult_male_18_60 = serializers.IntegerField(required=True)
    adult_female_18_60 = serializers.IntegerField(required=True)
    elderly_male_60_plus = serializers.IntegerField(required=True)
    elderly_female_60_plus = serializers.IntegerField(required=True)
    total_beneficiaries_reached = serializers.IntegerField(required=True)
    people_with_disability = serializers.IntegerField(required=True)
    is_mpc = serializers.BooleanField(required=True)
    modality = serializers.CharField(required=True)
    type_of_modality = serializers.CharField(required=True)
    delivery_mechanism = serializers.CharField(required=True)
    number_of_transfers = serializers.IntegerField(required=True)
    value_ssp = serializers.DecimalField(
        max_digits=20, decimal_places=4, required=True
    )
    value_usd = serializers.DecimalField(
        max_digits=20, decimal_places=4, required=True
    )
    comments = serializers.CharField(required=True, allow_blank=True)
    contribute_hrp_aap = serializers.CharField(required=True)
    hrp_aap_indicators = serializers.CharField(required=True)
    activity_type = serializers.CharField(required=True)
    sub_activity_type = serializers.CharField(required=True)
    measurements = serializers.CharField(required=True)
    achieved = serializers.IntegerField(required=True)
    column1 = serializers.CharField(required=True, allow_blank=True)
    boys_above_5 = serializers.IntegerField(required=True)
    girls_above_5 = serializers.IntegerField(required=True)
    boys_5_17 = serializers.IntegerField(required=True)
    girls_5_17 = serializers.IntegerField(required=True)
    men_18_59 = serializers.IntegerField(required=True)
    women_18_59 = serializers.IntegerField(required=True)
    men_60_plus = serializers.IntegerField(required=True)
    women_60_plus = serializers.IntegerField(required=True)
    total_reached_quarter = serializers.IntegerField(required=True)

    uploaded_by = UserMinSerializer(read_only=True)
    verified_by = UserMinSerializer(read_only=True)

    class Meta:
        model = FiveWActivity
        fields = "__all__"
        read_only_fields = [
            "id",
            "uploaded_by",
            "verified_by",
            "created_at",
            "updated_at",
        ]


class FiveWImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = FiveWImport
        fields = "__all__"
        read_only_fields = ("uploaded_by", "verified_by", "created_at", "updated_at")

    def validate_file(self, value):
        file_name = value.name.lower()
        if not file_name.endswith((".xlsx", ".xls", ".csv")):
            raise serializers.ValidationError(
                "Only Excel (.xlsx, .xls) or CSV (.csv) files are allowed."
            )

        # Check for missing required fields in Excel/CSV
        missing_errors = find_missing_required_fields(value)
        if missing_errors:
            # Return top 5 missing field errors for readability
            error_str = " | ".join(missing_errors[:5])
            if len(missing_errors) > 5:
                error_str += f" and {len(missing_errors) - 5} more errors"
            raise serializers.ValidationError(
                f"File validation failed due to missing required fields: {error_str}"
            )
        return value
