from rest_framework import serializers

from .models import ClusterContact


class ClusterContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClusterContact
        fields = [
            "id",
            "name",
            "email",
            "organization",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class SendClusterContactEmailSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=255)
    body = serializers.CharField()
    emails = serializers.ListField(
        child=serializers.EmailField(),
        required=False,
        default=list,
    )


class FileSerializer(serializers.Serializer):
    file = serializers.FileField(required=False)
