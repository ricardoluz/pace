from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    # IsAuthenticatedOrReadOnly,
)

#
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework import generics

#
from rest_framework.response import Response
from rest_framework import status

from pace.core.models import (
    Activity,
    UserSystem,
)
from pace.core.serializers import (
    ActivitySerializer,
    UserSystemSerializer,
)


class ActivityPagination(PageNumberPagination):
    page_size = 4


class ActivityViewSet(ModelViewSet):

    def get_queryset(self):
        # TODO: Review how to show only the user's own activities.
        qs = super().get_queryset()
        qs = qs.filter(owner=self.request.user)
        return qs

    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    pagination_class = ActivityPagination
    http_method_names = [
        "get",
        "post",
        "options",
        "head",
        "patch",
        "delete",
    ]

    # Only allow reading (access) when authenticated.
    permission_classes = [IsAuthenticated]

    # Overriding the create method to save the owner user.
    def create(self, request, *args, **kwargs):

        print(request.data)
        print("\n")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class UserSystemViewSet(ModelViewSet):

    def get_queryset(self):
        # TODO: Review how to show only the user's own activities.
        qs = super().get_queryset()
        # qs = qs.filter(owner=self.request.user)
        return qs

    queryset = UserSystem.objects.all()
    serializer_class = UserSystemSerializer
    pagination_class = ActivityPagination
    http_method_names = [
        "get",
        "post",
        "options",
        "head",
        "patch",
        "delete",
    ]

    # Only allow reading (access) when authenticated.
    permission_classes = [
        # IsAuthenticated,
        AllowAny,
        # IsAuthenticatedOrReadOnly
    ]

    # Overriding the create method to save the owner user.
    def create(self, request, *args, **kwargs):

        def createUser(validated_data):
            user = User.objects.create(
                username=validated_data["email"].lower(),
                email=validated_data["email"],
            )
            # TODO:
            user.set_password(validated_data["password"])
            user.save()

            return user

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=createUser(request.data))
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
