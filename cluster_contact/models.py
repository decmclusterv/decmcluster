from django.db import models


class ClusterContact(models.Model):
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    organization = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name
