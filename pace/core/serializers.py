# from datetime import datetime

#
from rest_framework import serializers

from pace.core.models import Activity


class ActivitySerializerBase(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    activity_date = serializers.DateTimeField(required=True)
    distance = serializers.FloatField(required=True)
    hours = serializers.IntegerField()
    minutes = serializers.IntegerField()
    seconds = serializers.IntegerField()

    class Meta:
        model = Activity
        fields = [
            "id",
            "activity_date",
            "distance",
            "hours",
            "minutes",
            "seconds",
        ]


class ActivitySerializerPost(ActivitySerializerBase):

    def create(self, validated_data):
        """
        Create and return a new `Activity` instance, given the validated data.
        """
        # print(validated_data)
        # validated_data.activity_date = datetime.utcnow()
        return Activity.objects.create(**validated_data)

    def update(self, validated_data):
        """
        Create and return a new `Activity` instance, given the validated data.
        """

        return Activity.objects.update(**validated_data)


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
        ]

    total_minutes = serializers.FloatField(read_only=True)
