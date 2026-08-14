from django.conf import settings
from django.db import models


class VillageAssessment(models.Model):
    # Survey metadata
    survey_start = models.DateField(null=True, blank=True)
    survey_end = models.DateField(null=True, blank=True)
    survey_date = models.DateField(null=True, blank=True)
    enumerator_username = models.CharField(max_length=255, null=True, blank=True)
    device_id = models.CharField(max_length=255, null=True, blank=True)
    audit_file = models.CharField(max_length=255, null=True, blank=True)
    audit_url = models.URLField(max_length=1000, null=True, blank=True)
    consent = models.TextField(null=True, blank=True)

    # Methodology
    methodology_individual_ki = models.CharField(max_length=255, null=True, blank=True)
    methodology_group_ki = models.CharField(max_length=255, null=True, blank=True)
    methodology_direct_observation = models.CharField(
        max_length=255, null=True, blank=True
    )
    methodology_other = models.CharField(max_length=255, null=True, blank=True)
    data_collection_method = models.CharField(max_length=255, null=True, blank=True)

    # Key Informants 1-6
    ki1_name = models.CharField(max_length=255, null=True, blank=True)
    ki1_type = models.CharField(max_length=100, null=True, blank=True)
    ki1_gender = models.CharField(max_length=50, null=True, blank=True)
    ki1_age = models.IntegerField(null=True, blank=True)
    ki1_contact = models.CharField(max_length=100, null=True, blank=True)

    ki2_name = models.CharField(max_length=255, null=True, blank=True)
    ki2_type = models.CharField(max_length=100, null=True, blank=True)
    ki2_gender = models.CharField(max_length=50, null=True, blank=True)
    ki2_age = models.IntegerField(null=True, blank=True)
    ki2_contact = models.CharField(max_length=100, null=True, blank=True)

    ki3_name = models.CharField(max_length=255, null=True, blank=True)
    ki3_type = models.CharField(max_length=100, null=True, blank=True)
    ki3_gender = models.CharField(max_length=50, null=True, blank=True)
    ki3_age = models.IntegerField(null=True, blank=True)
    ki3_contact = models.CharField(max_length=100, null=True, blank=True)

    ki4_name = models.CharField(max_length=255, null=True, blank=True)
    ki4_type = models.CharField(max_length=100, null=True, blank=True)
    ki4_gender = models.CharField(max_length=50, null=True, blank=True)
    ki4_age = models.IntegerField(null=True, blank=True)
    ki4_contact = models.CharField(max_length=100, null=True, blank=True)

    ki5_name = models.CharField(max_length=255, null=True, blank=True)
    ki5_type = models.CharField(max_length=100, null=True, blank=True)
    ki5_gender = models.CharField(max_length=50, null=True, blank=True)
    ki5_age = models.IntegerField(null=True, blank=True)
    ki5_contact = models.CharField(max_length=100, null=True, blank=True)

    ki6_name = models.CharField(max_length=255, null=True, blank=True)
    ki6_type = models.CharField(max_length=100, null=True, blank=True)
    ki6_gender = models.CharField(max_length=50, null=True, blank=True)
    ki6_age = models.IntegerField(null=True, blank=True)
    ki6_contact = models.CharField(max_length=100, null=True, blank=True)

    # Assessment details & enumerators
    assessment_date = models.DateField(null=True, blank=True, db_index=True)
    assessment_start_time = models.TimeField(null=True, blank=True)
    enumerator1_name = models.CharField(max_length=255, null=True, blank=True)
    enumerator1_phone = models.CharField(max_length=100, null=True, blank=True)
    enumerator1_gender = models.CharField(max_length=50, null=True, blank=True)
    enumerator2_name = models.CharField(max_length=255, null=True, blank=True)
    enumerator2_phone = models.CharField(max_length=100, null=True, blank=True)
    enumerator2_gender = models.CharField(max_length=50, null=True, blank=True)

    # Geographic info
    province = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    area_council = models.CharField(
        max_length=255, null=True, blank=True, db_index=True
    )
    village_name = models.CharField(
        max_length=255, null=True, blank=True, db_index=True
    )
    village_other = models.CharField(max_length=255, null=True, blank=True)
    village_condition = models.TextField(null=True, blank=True)

    # IDP statistics
    idp_present = models.BooleanField(null=True, blank=True, default=False)
    idp_households_total = models.IntegerField(null=True, blank=True, default=0)
    idp_infant_male = models.IntegerField(null=True, blank=True, default=0)
    idp_infant_female = models.IntegerField(null=True, blank=True, default=0)
    idp_child_1_5_male = models.IntegerField(null=True, blank=True, default=0)
    idp_child_1_5_female = models.IntegerField(null=True, blank=True, default=0)
    idp_child_6_12_male = models.IntegerField(null=True, blank=True, default=0)
    idp_child_6_12_female = models.IntegerField(null=True, blank=True, default=0)
    idp_adolescent_male = models.IntegerField(null=True, blank=True, default=0)
    idp_adolescent_female = models.IntegerField(null=True, blank=True, default=0)
    idp_adult_male = models.IntegerField(null=True, blank=True, default=0)
    idp_adult_female = models.IntegerField(null=True, blank=True, default=0)
    idp_elderly_male = models.IntegerField(null=True, blank=True, default=0)
    idp_elderly_female = models.IntegerField(null=True, blank=True, default=0)
    idp_male_total = models.IntegerField(null=True, blank=True, default=0)
    idp_female_total = models.IntegerField(null=True, blank=True, default=0)
    idp_individuals_total = models.IntegerField(null=True, blank=True, default=0)

    # Returnee statistics
    returnees_present = models.BooleanField(null=True, blank=True, default=False)
    returnee_households_total = models.IntegerField(null=True, blank=True, default=0)
    returnee_individuals_total = models.IntegerField(null=True, blank=True, default=0)

    # Vulnerabilities
    pregnant_women_count = models.IntegerField(null=True, blank=True, default=0)
    female_headed_hh = models.IntegerField(null=True, blank=True, default=0)
    elderly_headed_hh = models.IntegerField(null=True, blank=True, default=0)
    male_headed_hh = models.IntegerField(null=True, blank=True, default=0)
    child_headed_hh = models.IntegerField(null=True, blank=True, default=0)
    pwd_total = models.IntegerField(null=True, blank=True, default=0)
    idp_pwd_total = models.IntegerField(null=True, blank=True, default=0)

    # Shelter conditions
    shelter_primary = models.CharField(max_length=255, null=True, blank=True)
    shelter_secondary = models.CharField(max_length=255, null=True, blank=True)
    displacement_shelter_type = models.CharField(max_length=255, null=True, blank=True)
    displaced_hh_estimated = models.IntegerField(null=True, blank=True, default=0)
    displacement_duration = models.CharField(max_length=255, null=True, blank=True)
    housing_type_pre_cyclone = models.CharField(max_length=255, null=True, blank=True)
    house_rebuild_duration = models.CharField(max_length=255, null=True, blank=True)
    rebuild_material_type = models.CharField(max_length=255, null=True, blank=True)
    house_cyclone_resilience = models.CharField(max_length=255, null=True, blank=True)
    remaining_idp_intention = models.CharField(max_length=255, null=True, blank=True)

    # Community context
    seasonal_worker_level = models.CharField(max_length=255, null=True, blank=True)
    community_participation = models.CharField(max_length=255, null=True, blank=True)
    cdccc_exists = models.BooleanField(null=True, blank=True, default=False)
    early_warning_received = models.BooleanField(null=True, blank=True, default=False)
    annual_population_displaced = models.IntegerField(null=True, blank=True, default=0)

    # Needs
    top_need_1 = models.CharField(max_length=255, null=True, blank=True)
    top_need_2 = models.CharField(max_length=255, null=True, blank=True)
    top_need_3 = models.CharField(max_length=255, null=True, blank=True)

    # GPS info
    gps_latitude = models.DecimalField(
        max_digits=12, decimal_places=8, null=True, blank=True
    )
    gps_longitude = models.DecimalField(
        max_digits=12, decimal_places=8, null=True, blank=True
    )
    gps_altitude = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    gps_precision = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )

    # Submission & Record info
    record_id = models.CharField(max_length=100, null=True, blank=True)
    record_uuid = models.CharField(max_length=255, null=True, blank=True)
    submission_time = models.DateTimeField(null=True, blank=True)
    validation_status = models.CharField(
        max_length=100, null=True, blank=True, db_index=True
    )
    submission_status = models.CharField(max_length=100, null=True, blank=True)
    submitted_by = models.CharField(max_length=255, null=True, blank=True)
    form_version = models.CharField(max_length=100, null=True, blank=True)
    record_index = models.IntegerField(null=True, blank=True)

    class StatusChoices(models.TextChoices):
        UNVERIFIED = "unverified", "Unverified"
        VERIFIED = "verified", "Verified"
        RETURNED = "returned", "Returned"

    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.UNVERIFIED,
        db_index=True,
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="uploaded_village_assessments",
    )
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_village_assessments",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["province"]),
            models.Index(fields=["area_council"]),
            models.Index(fields=["village_name"]),
            models.Index(fields=["assessment_date"]),
            models.Index(fields=["validation_status"]),
            models.Index(fields=["status"]),
        ]
        verbose_name = "Village Assessment"
        verbose_name_plural = "Village Assessments"

    def __str__(self):
        return f"{self.village_name or 'N/A'} - {self.assessment_date or 'N/A'}"


class VillageAssessmentImport(models.Model):
    class StatusChoices(models.TextChoices):
        UNVERIFIED = "unverified", "Unverified"
        VERIFIED = "verified", "Verified"
        RETURNED = "returned", "Returned"

    name = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(upload_to="village_assessment_imports/")
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.UNVERIFIED,
        db_index=True,
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="uploaded_village_assessment_imports",
    )
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_village_assessment_imports",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["status", "created_at"]),
        ]
        verbose_name = "Village Assessment Import"
        verbose_name_plural = "Village Assessment Imports"

    def __str__(self):
        return f"Village Assessment Import Request #{self.id} - {self.file.name}"
