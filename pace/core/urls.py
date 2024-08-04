from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from pace.core.views import ActivityList, ActivityDetail, Activity
from pace.core.serializers import ActivitySerializer

urlpatterns = [
    path("activities/", ActivityList.as_view()),
    path("activities/<int:pk>/", ActivityDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
