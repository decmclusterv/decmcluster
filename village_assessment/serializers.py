from rest_framework import serializers

from .models import VillageAssessment, VillageAssessmentImport
from .services.import_service import find_missing_required_fields


from displacement.serializers import UserMinSerializer


class VillageAssessmentSerializer(serializers.ModelSerializer):
    # Enforce required constraints at the API level (DB remains nullable for existing data)
    survey_start = serializers.DateField(required=True)
    survey_end = serializers.DateField(required=True)
    survey_date = serializers.DateField(required=True)
    enumerator_username = serializers.CharField(required=True)
    device_id = serializers.CharField(required=True)
    audit_file = serializers.CharField(required=True)
    audit_url = serializers.URLField(required=True)
    consent = serializers.CharField(required=True)
    methodology_individual_ki = serializers.CharField(required=True)
    methodology_group_ki = serializers.CharField(required=True)
    methodology_direct_observation = serializers.CharField(required=True)
    methodology_other = serializers.CharField(required=True)
    data_collection_method = serializers.CharField(required=True)
    ki1_name = serializers.CharField(required=True)
    ki1_type = serializers.CharField(required=True)
    ki1_gender = serializers.CharField(required=True)
    ki1_age = serializers.IntegerField(required=True)
    ki1_contact = serializers.CharField(required=True)
    ki2_name = serializers.CharField(required=True)
    ki2_type = serializers.CharField(required=True)
    ki2_gender = serializers.CharField(required=True)
    ki2_age = serializers.IntegerField(required=True)
    ki2_contact = serializers.CharField(required=True)
    ki3_name = serializers.CharField(required=True)
    ki3_type = serializers.CharField(required=True)
    ki3_gender = serializers.CharField(required=True)
    ki3_age = serializers.IntegerField(required=True)
    ki3_contact = serializers.CharField(required=True)
    ki4_name = serializers.CharField(required=True)
    ki4_type = serializers.CharField(required=True)
    ki4_gender = serializers.CharField(required=True)
    ki4_age = serializers.IntegerField(required=True)
    ki4_contact = serializers.CharField(required=True)
    ki5_name = serializers.CharField(required=True)
    ki5_type = serializers.CharField(required=True)
    ki5_gender = serializers.CharField(required=True)
    ki5_age = serializers.IntegerField(required=True)
    ki5_contact = serializers.CharField(required=True)
    ki6_name = serializers.CharField(required=True)
    ki6_type = serializers.CharField(required=True)
    ki6_gender = serializers.CharField(required=True)
    ki6_age = serializers.IntegerField(required=True)
    ki6_contact = serializers.CharField(required=True)
    assessment_date = serializers.DateField(required=True)
    assessment_start_time = serializers.TimeField(required=True)
    enumerator1_name = serializers.CharField(required=True)
    enumerator1_phone = serializers.CharField(required=True)
    enumerator1_gender = serializers.CharField(required=True)
    enumerator2_name = serializers.CharField(required=True)
    enumerator2_phone = serializers.CharField(required=True)
    enumerator2_gender = serializers.CharField(required=True)
    province = serializers.CharField(required=True)
    area_council = serializers.CharField(required=True)
    village_name = serializers.CharField(required=True)
    village_other = serializers.CharField(required=True)
    village_condition = serializers.CharField(required=True)
    idp_present = serializers.BooleanField(required=True)
    idp_households_total = serializers.IntegerField(required=True)
    idp_infant_male = serializers.IntegerField(required=True)
    idp_infant_female = serializers.IntegerField(required=True)
    idp_child_1_5_male = serializers.IntegerField(required=True)
    idp_child_1_5_female = serializers.IntegerField(required=True)
    idp_child_6_12_male = serializers.IntegerField(required=True)
    idp_child_6_12_female = serializers.IntegerField(required=True)
    idp_adolescent_male = serializers.IntegerField(required=True)
    idp_adolescent_female = serializers.IntegerField(required=True)
    idp_adult_male = serializers.IntegerField(required=True)
    idp_adult_female = serializers.IntegerField(required=True)
    idp_elderly_male = serializers.IntegerField(required=True)
    idp_elderly_female = serializers.IntegerField(required=True)
    idp_male_total = serializers.IntegerField(required=True)
    idp_female_total = serializers.IntegerField(required=True)
    idp_individuals_total = serializers.IntegerField(required=True)
    returnees_present = serializers.BooleanField(required=True)
    returnee_households_total = serializers.IntegerField(required=True)
    returnee_individuals_total = serializers.IntegerField(required=True)
    pregnant_women_count = serializers.IntegerField(required=True)
    female_headed_hh = serializers.IntegerField(required=True)
    elderly_headed_hh = serializers.IntegerField(required=True)
    male_headed_hh = serializers.IntegerField(required=True)
    child_headed_hh = serializers.IntegerField(required=True)
    pwd_total = serializers.IntegerField(required=True)
    idp_pwd_total = serializers.IntegerField(required=True)
    shelter_primary = serializers.CharField(required=True)
    shelter_secondary = serializers.CharField(required=True)
    displacement_shelter_type = serializers.CharField(required=True)
    displaced_hh_estimated = serializers.IntegerField(required=True)
    displacement_duration = serializers.CharField(required=True)
    housing_type_pre_cyclone = serializers.CharField(required=True)
    house_rebuild_duration = serializers.CharField(required=True)
    rebuild_material_type = serializers.CharField(required=True)
    house_cyclone_resilience = serializers.CharField(required=True)
    remaining_idp_intention = serializers.CharField(required=True)
    seasonal_worker_level = serializers.CharField(required=True)
    community_participation = serializers.CharField(required=True)
    cdccc_exists = serializers.BooleanField(required=True)
    early_warning_received = serializers.BooleanField(required=True)
    annual_population_displaced = serializers.IntegerField(required=True)
    top_need_1 = serializers.CharField(required=True)
    top_need_2 = serializers.CharField(required=True)
    top_need_3 = serializers.CharField(required=True)
    gps_latitude = serializers.DecimalField(max_digits=12, decimal_places=8, required=True)
    gps_longitude = serializers.DecimalField(max_digits=12, decimal_places=8, required=True)
    gps_altitude = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    gps_precision = serializers.DecimalField(max_digits=8, decimal_places=2, required=True)
    record_id = serializers.CharField(required=True)
    record_uuid = serializers.CharField(required=True)
    submission_time = serializers.DateTimeField(required=True)
    validation_status = serializers.CharField(required=True)
    submission_status = serializers.CharField(required=True)
    submitted_by = serializers.CharField(required=True)
    form_version = serializers.CharField(required=True)
    record_index = serializers.IntegerField(required=True)

    uploaded_by = UserMinSerializer(read_only=True)
    verified_by = UserMinSerializer(read_only=True)

    class Meta:
        model = VillageAssessment
        fields = "__all__"
        read_only_fields = [
            "id",
            "uploaded_by",
            "verified_by",
            "created_at",
            "updated_at",
        ]


class VillageAssessmentImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = VillageAssessmentImport
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
            error_str = " | ".join(missing_errors[:5])
            if len(missing_errors) > 5:
                error_str += f" and {len(missing_errors) - 5} more errors"
            raise serializers.ValidationError(
                f"File validation failed due to missing required fields: {error_str}"
            )
        return value
