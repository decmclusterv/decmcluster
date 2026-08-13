from django.db import models


class BaseDisplacementForm(models.Model):
    field = models.JSONField(
        default=dict,
        blank=True,
        null=True,
        help_text="Form field definitions and schema configuration.",
    )
    data = models.JSONField(
        default=dict,
        blank=True,
        null=True,
        help_text="Submitted data and form responses.",
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class DurableSolutionRelocationSurvey(BaseDisplacementForm):
    class Meta(BaseDisplacementForm.Meta):
        verbose_name = "Durable Solution & Relocation Survey"
        verbose_name_plural = "Durable Solution & Relocation Surveys"

    def __str__(self):
        return f"Durable Solution & Relocation Survey #{self.pk}"


class ServiceMonitoringTool2026(BaseDisplacementForm):
    class Meta(BaseDisplacementForm.Meta):
        verbose_name = "Service Monitoring Tool 2026"
        verbose_name_plural = "Service Monitoring Tools 2026"

    def __str__(self):
        return f"Service Monitoring Tool 2026 #{self.pk}"


class DisplacementTrackingMatrixForm(BaseDisplacementForm):
    class Meta(BaseDisplacementForm.Meta):
        verbose_name = "Displacement Tracking Matrix Form"
        verbose_name_plural = "Displacement Tracking Matrix Forms"

    def __str__(self):
        return f"Displacement Tracking Matrix Form #{self.pk}"


class RapidAssessmentFormAreaCouncil(BaseDisplacementForm):
    class Meta(BaseDisplacementForm.Meta):
        verbose_name = "Rapid Assessment Form (Area Council)"
        verbose_name_plural = "Rapid Assessment Forms (Area Council)"

    def __str__(self):
        return f"Rapid Assessment Form (Area Council) #{self.pk}"


class CommunityLevelDamageAssessmentForm(BaseDisplacementForm):
    class Meta(BaseDisplacementForm.Meta):
        verbose_name = "Community Level Damage Assessment Form"
        verbose_name_plural = "Community Level Damage Assessment Forms"

    def __str__(self):
        return f"Community Level Damage Assessment Form #{self.pk}"


class DisplacementProfilePhoneSurvey(BaseDisplacementForm):
    class Meta(BaseDisplacementForm.Meta):
        verbose_name = "Displacement Profile - Phone Survey"
        verbose_name_plural = "Displacement Profile - Phone Surveys"

    def __str__(self):
        return f"Displacement Profile - Phone Survey #{self.pk}"


class DamageAssessmentFormCommunityV2(BaseDisplacementForm):
    class Meta(BaseDisplacementForm.Meta):
        verbose_name = "Damage Assessment Form (Community V2)"
        verbose_name_plural = "Damage Assessment Forms (Community V2)"

    def __str__(self):
        return f"Damage Assessment Form (Community V2) #{self.pk}"
