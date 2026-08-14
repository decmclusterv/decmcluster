from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from decmcluster.services.email_service import send_status_update_email

from .models import VillageAssessmentImport
from .services.import_service import (
    import_village_assessments_from_csv,
    import_village_assessments_from_excel,
    find_missing_required_fields,
)
from .utils import send_village_assessment_import_verification_email


@receiver(pre_save, sender=VillageAssessmentImport)
def capture_old_status(sender, instance, **kwargs):
    """
    Pre-save receiver to capture the status of the import before saving.
    """
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            instance._old_status = old_instance.status
        except sender.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None


@receiver(post_save, sender=VillageAssessmentImport)
def handle_import_status_change(sender, instance, created, **kwargs):
    """
    Post-save receiver to:
    - Send notification email to admin when created.
    - Run the import logic when verified.
    - Notify the uploader on status change (verified/returned).
    """
    if created:
        send_village_assessment_import_verification_email(instance)
        return

    old_status = getattr(instance, "_old_status", None)
    if old_status and instance.status != old_status:
        if instance.status == VillageAssessmentImport.StatusChoices.VERIFIED:
            # Open file and run the appropriate import service
            if instance.file:
                instance.file.open()
                try:
                    # Run missing required fields validation check
                    errors = find_missing_required_fields(instance.file)
                    if errors:
                        raise ValidationError(
                            f"Cannot verify: spreadsheet has missing fields: {errors[0]}"
                        )

                    file_name = instance.file.name.lower()
                    if file_name.endswith(".csv"):
                        import_village_assessments_from_csv(
                            instance.file,
                            uploaded_by=instance.uploaded_by,
                            verified_by=instance.verified_by,
                        )
                    else:
                        import_village_assessments_from_excel(
                            instance.file,
                            uploaded_by=instance.uploaded_by,
                            verified_by=instance.verified_by,
                        )
                finally:
                    instance.file.close()

            # Send notification to uploader
            send_status_update_email(
                instance=instance,
                model_name="Village Assessment Import",
                new_status=instance.status,
            )

        elif instance.status == VillageAssessmentImport.StatusChoices.RETURNED:
            # Send notification to uploader
            send_status_update_email(
                instance=instance,
                model_name="Village Assessment Import",
                new_status=instance.status,
            )


from .models import VillageAssessment


@receiver(pre_save, sender=VillageAssessment)
def capture_village_old_status(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            instance._old_status = old_instance.status
        except sender.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None


@receiver(post_save, sender=VillageAssessment)
def handle_village_status_change(sender, instance, created, **kwargs):
    if created:
        return
    old_status = getattr(instance, "_old_status", None)
    if old_status and instance.status != old_status:
        if instance.status in (
            VillageAssessment.StatusChoices.VERIFIED,
            VillageAssessment.StatusChoices.RETURNED,
        ):
            send_status_update_email(
                instance=instance,
                model_name="Village Assessment",
                new_status=instance.status,
            )
