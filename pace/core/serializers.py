from rest_framework import serializers

#
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

#
from pace.core.models import Activity, UserSystem


class ActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = [
            "id",
            "activity_date",
            "distance",
            "hours",
            "minutes",
            "seconds",
            "total_minutes",
            "owner",
        ]

    total_minutes = serializers.FloatField(read_only=True)


class UserSystemSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        # max_length=132,
        # required=True,
        read_only=True,
    )

    class Meta:
        model = UserSystem
        read_only = True
        fields = (
            "id",
            "name",
            "last_name",
            "nick_name",
            "email",
            "password",
        )
        read_only_fields = ["password"]
        # extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        if len(data["last_name"]) < 0:
            raise serializers.ValidationError("Error ........")
        return data


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "password2",
            "email",
            "first_name",
            "last_name",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user
