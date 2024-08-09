from django.urls import include, path

# from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import SimpleRouter

from pace.core.views import (
    ActivityList,
    ActivityDetail,
    Activity,
    ActivityViewSet,
)
from pace.core.serializers import ActivitySerializer

app_name = "core"

activity_api_router = SimpleRouter()

activity_api_router.register(
    prefix="activity/api",
    viewset=ActivityViewSet,
    basename="activity-api",
)

urlpatterns = [
    # path("admin/", admin.site.urls),
    # path("activities/", ActivityList.as_view()),
    # path("activities/<int:pk>/", ActivityDetail.as_view()),
    path("", include(activity_api_router.urls)),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
