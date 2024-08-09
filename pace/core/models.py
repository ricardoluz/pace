from django.db import models
from django.contrib.auth.models import User


class Activity(models.Model):
    activity_date = models.DateTimeField(null=False)
    distance = models.FloatField(null=False)
    hours = models.IntegerField(null=False, default=0)
    minutes = models.IntegerField(null=False, default=0)
    seconds = models.IntegerField(null=False, default=0)

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def total_minutes(self):
        return round(self.hours * 60 + self.minutes + self.seconds / 60, 2)

    # owner = models.ForeignKey(
    #     "auth.User",
    #     related_name="snippets",
    #     on_delete=models.CASCADE,
    # )

    # class Meta:
    #     ordering = ["id"]

    def __str__(self):
        return f"Distance: {self.distance} | time: {self.hours}:\
            {self.minutes}:\
            {self.seconds}"
