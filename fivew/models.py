from django.conf import settings
from django.db import models


class FiveWActivity(models.Model):
    donor = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    donor_names = models.CharField(max_length=255, null=True, blank=True)
    reporting_org_name = models.CharField(
        max_length=255, null=True, blank=True, db_index=True
    )
    ro_code = models.CharField(max_length=100, null=True, blank=True)
    reporting_org_type = models.CharField(max_length=255, null=True, blank=True)
    other_ip_name = models.CharField(max_length=255, null=True, blank=True)
    ip_code = models.CharField(max_length=100, null=True, blank=True)
    ip_type = models.CharField(max_length=255, null=True, blank=True)
    reporting_month = models.CharField(
        max_length=50, null=True, blank=True, db_index=True
    )
    activity_status = models.CharField(
        max_length=100, null=True, blank=True, db_index=True
    )
    state_abyei = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    admin1_code = models.CharField(max_length=100, null=True, blank=True)
    province = models.CharField(max_length=255, null=True, blank=True)
    admin2_code = models.CharField(max_length=100, null=True, blank=True)
    location_evac_name = models.CharField(max_length=255, null=True, blank=True)
    cluster_name = models.CharField(
        max_length=255, null=True, blank=True, db_index=True
    )
    hrp_non_hrp = models.CharField(max_length=50, null=True, blank=True)
    project_number = models.CharField(max_length=100, null=True, blank=True)
    project_name = models.CharField(max_length=255, null=True, blank=True)
    activity = models.TextField(null=True, blank=True)
    indicator = models.TextField(null=True, blank=True)
    unit = models.CharField(max_length=100, null=True, blank=True)
    target = models.IntegerField(null=True, blank=True, default=0)
    total_value = models.DecimalField(
        max_digits=20, decimal_places=4, null=True, blank=True
    )
    new_beneficiaries = models.BooleanField(null=True, blank=True)
    beneficiaries_type_under_18 = models.CharField(
        max_length=100, null=True, blank=True
    )
    child_male_under_18 = models.IntegerField(null=True, blank=True, default=0)
    child_female_under_18 = models.IntegerField(null=True, blank=True, default=0)
    adult_male_18_60 = models.IntegerField(null=True, blank=True, default=0)
    adult_female_18_60 = models.IntegerField(null=True, blank=True, default=0)
    elderly_male_60_plus = models.IntegerField(null=True, blank=True, default=0)
    elderly_female_60_plus = models.IntegerField(null=True, blank=True, default=0)
    total_beneficiaries_reached = models.IntegerField(null=True, blank=True, default=0)
    people_with_disability = models.IntegerField(null=True, blank=True, default=0)
    is_mpc = models.BooleanField(null=True, blank=True)
    modality = models.CharField(max_length=100, null=True, blank=True)
    type_of_modality = models.CharField(max_length=100, null=True, blank=True)
    delivery_mechanism = models.CharField(max_length=255, null=True, blank=True)
    number_of_transfers = models.IntegerField(null=True, blank=True, default=0)
    value_ssp = models.DecimalField(
        max_digits=20, decimal_places=4, null=True, blank=True
    )
    value_usd = models.DecimalField(
        max_digits=20, decimal_places=4, null=True, blank=True
    )
    comments = models.TextField(null=True, blank=True)
    contribute_hrp_aap = models.CharField(max_length=100, null=True, blank=True)
    hrp_aap_indicators = models.TextField(null=True, blank=True)
    activity_type = models.CharField(max_length=255, null=True, blank=True)
    sub_activity_type = models.CharField(max_length=255, null=True, blank=True)
    measurements = models.CharField(max_length=255, null=True, blank=True)
    achieved = models.IntegerField(null=True, blank=True, default=0)
    column1 = models.CharField(max_length=255, null=True, blank=True)
    boys_above_5 = models.IntegerField(null=True, blank=True, default=0)
    girls_above_5 = models.IntegerField(null=True, blank=True, default=0)
    boys_5_17 = models.IntegerField(null=True, blank=True, default=0)
    girls_5_17 = models.IntegerField(null=True, blank=True, default=0)
    men_18_59 = models.IntegerField(null=True, blank=True, default=0)
    women_18_59 = models.IntegerField(null=True, blank=True, default=0)
    men_60_plus = models.IntegerField(null=True, blank=True, default=0)
    women_60_plus = models.IntegerField(null=True, blank=True, default=0)
    total_reached_quarter = models.IntegerField(null=True, blank=True, default=0)

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
        related_name="uploaded_fivew_activities",
    )
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_fivew_activities",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["donor"]),
            models.Index(fields=["reporting_org_name"]),
            models.Index(fields=["reporting_month"]),
            models.Index(fields=["activity_status"]),
            models.Index(fields=["state_abyei"]),
            models.Index(fields=["cluster_name"]),
            models.Index(fields=["status"]),
        ]
        verbose_name = "5W Activity"
        verbose_name_plural = "5W Activities"

    def __str__(self):
        return f"{self.reporting_org_name} - {self.activity} - {self.reporting_month}"


class FiveWImport(models.Model):
    class StatusChoices(models.TextChoices):
        UNVERIFIED = "unverified", "Unverified"
        VERIFIED = "verified", "Verified"
        RETURNED = "returned", "Returned"

    name = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(upload_to="fivew_imports/")
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
        related_name="uploaded_fivew_imports",
    )
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_fivew_imports",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["status", "created_at"]),
        ]
        verbose_name = "5W Import"
        verbose_name_plural = "5W Imports"

    def __str__(self):
        return f"5W Import Request #{self.id} - {self.file.name}"
