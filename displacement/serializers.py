from rest_framework import serializers

from .models import Displacement, DisplacementImport
from .services.import_service import find_missing_required_fields


class DisplacementSerializer(serializers.ModelSerializer):
    # Enforce API validation required constraints for all nullable fields
    operation_code = serializers.CharField(required=True)
    admin0_name = serializers.CharField(required=True)
    admin0_pcode = serializers.CharField(required=True)
    admin1_name = serializers.CharField(required=True)
    admin1_pcode = serializers.CharField(required=True)
    admin2_name = serializers.CharField(required=True)
    admin2_pcode = serializers.CharField(required=True)
    admin_level = serializers.IntegerField(required=True)
    num_present_idps = serializers.IntegerField(required=True)
    reporting_date = serializers.DateField(required=True)
    reporting_year = serializers.IntegerField(required=True)
    reporting_month = serializers.IntegerField(required=True)
    round_number = serializers.IntegerField(required=True)
    displacement_reason = serializers.CharField(required=True)
    males_number = serializers.IntegerField(required=True)
    female_number = serializers.IntegerField(required=True)
    males_number_0_4 = serializers.IntegerField(required=True)
    females_number_0_4 = serializers.IntegerField(required=True)
    males_number_5_17 = serializers.IntegerField(required=True)
    females_number_5_17 = serializers.IntegerField(required=True)
    males_number_18_59 = serializers.IntegerField(required=True)
    females_number_18_59 = serializers.IntegerField(required=True)
    males_number_60_plus = serializers.IntegerField(required=True)
    females_number_60_plus = serializers.IntegerField(required=True)
    total_vul_hhs = serializers.IntegerField(required=True)
    idp_origin_admin1_name = serializers.CharField(required=True)
    idp_origin_admin1_pcode = serializers.CharField(required=True)
    assessment_type = serializers.CharField(required=True)
    operation_status = serializers.ChoiceField(
        choices=Displacement.OPERATION_STATUS, required=True
    )
    idp_destination = serializers.CharField(required=True)
    idp_destination_admin1_name = serializers.CharField(required=True)
    idp_destination_admin1_pcode = serializers.CharField(required=True)

    class Meta:
        model = Displacement
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class FileImportSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_blank=True)
    file = serializers.FileField()

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


class DisplacementImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisplacementImport
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "verified_by"]
