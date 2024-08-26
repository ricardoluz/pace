# from django.http import Http404
import uuid

#
# from rest_framework.views import APIView
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
# from rest_framework.decorators import api_view
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


# class ActivityList(APIView):
#     """
#     List all activities, or create a new activity.
#     """

#     def get(self, request, format=None):
#         activities = Activity.objects.all()
#         serializer = ActivitySerializer(activities, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = ActivitySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ActivityDetail(APIView):
#     """
#     Retrieve, update or delete a activity instance.
#     """

#     def get_object(self, pk):
#         try:
#             return Activity.objects.get(pk=pk)
#         except Activity.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         activity = self.get_object(pk)
#         serializer = ActivitySerializer(activity)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         activity = self.get_object(pk)
#         serializer = ActivitySerializer(activity, data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         activity = self.get_object(pk)
#         activity.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


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
            # print(validated_data)
            # tmp = validated_data["email"].split("@")[0]
            # print(tmp)
            user = User.objects.create(
                username=str(uuid.uuid4()),
                email=validated_data["email"],
            )

            user.set_password(validated_data["password"])
            user.save()

            return user

        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create User.
        id = createUser(request.data)
        print(id)

        # serializer.save()
        serializer.save(user=id)
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
