from django.db import models

# Create your models here.
class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    is_subscribed = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = "Newsletter"
        verbose_name_plural = "Newsletter"
    