from rest_framework import serializers

from pace.core.models import Activity


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
