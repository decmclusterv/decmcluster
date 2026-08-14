from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.


class EvacuationCentre(models.Model):
    country = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    agency = models.CharField(max_length=255)
    compound_name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    province = models.CharField(max_length=255)
    area_council = models.CharField(max_length=255)
    island = models.CharField(max_length=255, null=True, blank=True)
    village = models.CharField(max_length=255, null=True, blank=True)
    primary_contact = models.CharField(max_length=255, null=True, blank=True)
    secondary_contact = models.CharField(max_length=255, null=True, blank=True)
    compound_function = models.CharField(max_length=255, null=True, blank=True)
    is_ec_owner_approved = models.BooleanField(default=False)
    is_ec_govt_approved = models.BooleanField(default=False)
    name_of_outside_temporary_shelter = models.CharField(max_length=255, null=True, blank=True)
    outside_temporary_shelter_capacity = models.IntegerField(null=True, blank=True)
    first_aid_kit_availability = models.BooleanField(default=False)
    first_aid_trained_person = models.BooleanField(default=False)
    electricity_source = models.CharField(max_length=255, null=True, blank=True)
    drinking_water_source = models.CharField(max_length=255, null=True, blank=True)
    washing_water_source = models.CharField(max_length=255, null=True, blank=True)
    water_storage_capacity_litres = models.IntegerField(null=True, blank=True)
    no_of_buildings = models.IntegerField(null=True, blank=True)
    no_of_rooms = models.IntegerField(null=True, blank=True)
    internal_building_evacuee_capacity = models.IntegerField(null=True, blank=True)
    disaster_suitable_for = models.CharField(max_length=255, null=True, blank=True)
    enginerring_certified_cyclone_rating = models.CharField(max_length=255, null=True, blank=True)
    total_mens_toilet = models.IntegerField(null=True, blank=True)
    total_womens_toilet = models.IntegerField(null=True, blank=True)
    total_unisex_toilet = models.IntegerField(null=True, blank=True)
    total_disability_access_toilet = models.IntegerField(null=True, blank=True)
    total_mens_shower = models.IntegerField(null=True, blank=True)
    total_womens_shower = models.IntegerField(null=True, blank=True)
    total_unisex_shower = models.IntegerField(null=True, blank=True)
    total_disability_access_shower = models.IntegerField(null=True, blank=True)
    kitchen_cooking_facilities = models.BooleanField(default=False)
    laundry_facilities = models.BooleanField(default=False)
    communication_back_up = models.CharField(max_length=255, null=True, blank=True)
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
        related_name="uploaded_evacuation_centres",
    )
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_evacuation_centres",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["compound_name"]),
            models.Index(fields=["latitude", "longitude"]),
            models.Index(fields=["status"]),
        ]

    def clean(self):
        super().clean()
        if self.compound_name:
            qs = EvacuationCentre.objects.filter(
                compound_name__iexact=self.compound_name.strip()
            )
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError({
                    "compound_name": "Duplicate data: An evacuation centre with this compound name already exists."
                })

    def __str__(self):
        return f"{self.compound_name} - {self.organization}"


class EvacuationCentreImport(models.Model):
    class StatusChoices(models.TextChoices):
        UNVERIFIED = "unverified", "Unverified"
        VERIFIED = "verified", "Verified"
        RETURNED = "returned", "Returned"

    name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    file = models.FileField(upload_to="evacuation_centre_imports/")
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
        related_name="uploaded_evacuation_centre_imports",
    )
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_evacuation_centre_imports",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["status", "created_at"]),
        ]

    def __str__(self):
        return f"Import Request #{self.id} - {self.file.name}"
