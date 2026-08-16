from rest_framework import serializers

from .models import Newsletter
from .services.newsletter_service import subscribe_email


class NewsletterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = Newsletter
        fields = ["id", "email", "is_subscribed", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_email(self, value):
        email = value.lower().strip()
        
        # Check database for existing records with this email
        existing_subscriptions = Newsletter.objects.filter(email=email)
        
        # If we are updating an existing instance, exclude it from check
        if self.instance:
            existing_subscriptions = existing_subscriptions.exclude(pk=self.instance.pk)
            
        if existing_subscriptions.exists():
            # If there's an active subscription, raise validation error
            if existing_subscriptions.filter(is_subscribed=True).exists():
                raise serializers.ValidationError("This email is already subscribed.")
            
            # If the user is trying to update a record's email to an existing inactive one,
            # we should raise an error to enforce database uniqueness, except in the create flow
            if self.instance:
                raise serializers.ValidationError("A subscription with this email already exists.")
                
        return email

    def create(self, validated_data):
        email = validated_data.get("email")
        return subscribe_email(email)


class SendNewsletterEmailSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=255, required=True)
    body = serializers.CharField(required=True)
    emails = serializers.ListField(
        child=serializers.EmailField(),
        required=False,
        allow_empty=True,
        default=list,
    )


class NewsletterSubscriptionUpdateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    is_subscribed = serializers.BooleanField(required=True)

    def validate_email(self, value):
        return value.lower().strip()


