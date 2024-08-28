from django.db import models
from django.contrib.auth.models import User


class UserSystem(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True, null=False)
    name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=150, blank=True)
    nick_name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.last_name


class Activity(models.Model):
    activity_date = models.DateTimeField(null=False)
    distance = models.FloatField(null=False)
    hours = models.IntegerField(null=False)
    minutes = models.IntegerField(null=False)
    seconds = models.IntegerField(null=False)

    # TODO: Change User to UserSystem.
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

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
