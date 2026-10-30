from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model for Vanuatu CIM.
    Extend this model with additional fields as required by the application.
    """

    class Role(models.TextChoices):
        SUPERADMIN = "superadmin", "Superadmin"
        AREA_ADMINISTRATOR = "area_administrator", "Area Administrator"
        VIEWER = "viewer", "Viewer"
        DATA_ENUMERATOR = "data_enumerator", "Data Enumerator"
        FIELD_COORDINATOR = "field_coordinator", "Field Coordinator"
        EC_FOCAL_POINT = "ec_focal_point", "EC Focal Point"

    role = models.CharField(
        max_length=50,
        choices=Role.choices,
        default=Role.VIEWER,
        db_index=True,
    )
    access_control = models.JSONField(default=list, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.role == self.Role.SUPERADMIN:
            self.is_staff = True
            self.is_superuser = True
        elif not self.pk and (self.is_superuser or self.is_staff):
            self.role = self.Role.SUPERADMIN
            self.is_staff = True
            self.is_superuser = True
        else:
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
