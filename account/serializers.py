from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=False, required=False)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "access_control",
            "role",
        )
        extra_kwargs = {
            "email": {"required": True, "allow_blank": False},
            "first_name": {"required": False, "allow_blank": True},
            "last_name": {"required": False, "allow_blank": True},
            "is_active": {"required": False, "default": False},
            "access_control": {"required": False},
            "role": {"required": False},
        }

    def validate_role(self, value):
        request = self.context.get("request")
        if value == User.Role.SUPERADMIN:
            if (
                not request
                or not request.user
                or not (
                    request.user.is_authenticated
                    and (
                        request.user.role == User.Role.SUPERADMIN
                        or request.user.is_staff
                        or request.user.is_superuser
                    )
                )
            ):
                raise serializers.ValidationError(
                    "Only superadmins can create superadmin accounts."
                )
        return value

    def validate_email(self, value):
        if User.objects.filter(
            Q(email__iexact=value) | Q(username__iexact=value)
        ).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        email = validated_data["email"]
        is_active = validated_data.get("is_active", False)

        # Create user with username same as email, dynamic is_active state, and role
        user = User.objects.create_user(
            username=email,
            email=email,
            password=None,
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            is_active=is_active,
            access_control=validated_data.get("access_control", []),
            role=validated_data.get("role", User.Role.VIEWER),
        )

        user.set_unusable_password()
        user.save(update_fields=["password"])

        # Only send verification email if user is created as inactive
        if not user.is_active:
            from account.services.user_service import send_verification_email

            send_verification_email(user)

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        # Find active user by email only
        user = User.objects.filter(email__iexact=email).first()

        if not user or not user.check_password(password):
            raise serializers.ValidationError({
                "non_field_errors": ["Invalid credentials."]
            })
        if not user.is_active:
            raise serializers.ValidationError({
                "non_field_errors": ["Invalid credentials."]
            })

        # Generate Simple JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        # Inject custom claims into the access token
        access_token["id"] = user.id
        access_token["username"] = user.username
        access_token["email"] = user.email
        access_token["first_name"] = user.first_name
        access_token["last_name"] = user.last_name
        access_token["is_active"] = user.is_active
        access_token["role"] = user.role
        access_token["is_staff"] = user.is_staff
        access_token["is_superuser"] = user.is_superuser
        access_token["access_control"] = user.access_control

        return {
            "refresh": str(refresh),
            "access": str(access_token),
        }


class SuperAdminUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_active",
            "is_superuser",
            "is_staff",
            "access_control",
            "role",
            "date_joined",
        )
        read_only_fields = ("date_joined",)

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save(update_fields=["password"])
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save(update_fields=["password"])
        return user
