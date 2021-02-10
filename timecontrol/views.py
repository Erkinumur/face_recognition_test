from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import TimecontrolProfileDateFilter
from .permissions import SubscribtionIsActive
from .serializers import TimecontrolSerializer, ProfileCreateSerializer, \
    ProfileSerializer, CompanySerializer
from .utils import post_timecontrol_api_view_response, \
    get_timecontrol_api_view_response
from .models import Profile, TimeControl


class TimecontrolApiView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        value = request.data.get('value')
        profile = get_object_or_404(Profile.objects.all(), pk=pk)
        return post_timecontrol_api_view_response(profile, value)

    def get(self, request, pk, format=None):
        profile = get_object_or_404(Profile.objects.all(), pk=pk)
        return get_timecontrol_api_view_response(profile)


class TimecontrolListAPIView(generics.ListAPIView):
    serializer_class = TimecontrolSerializer
    # permission_classes = [IsAdminUser]
    filterset_class = TimecontrolProfileDateFilter

    def get_queryset(self):
        user = self.request.user
        company = self.request.user.profile.company
        if user.is_staff:
            queryset = TimeControl.objects.filter(
                profile__company=company).order_by('incoming')
        else:
            queryset = TimeControl.objects.filter(
                profile=user.profile,
                profile__company=company).order_by('incoming')
        return queryset


class ProfileCreateAPIView(generics.CreateAPIView):
    serializer_class = ProfileCreateSerializer
    permission_classes = [IsAdminUser]

    # def create(self, request, *args, **kwargs):
    #     print(f'request: {request.data}')
    #     return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        company = self.request.user.profile.company
        serializer.save(company=company)

        

class UserDeleteAPIView(generics.DestroyAPIView):
    queryset = Profile.objects.all()
    permission_classes = [IsAdminUser, SubscribtionIsActive]

    def perform_destroy(self, instance):
        user = instance.user
        user.delete()


class ProfileListAPIView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminUser, SubscribtionIsActive]

    def get_queryset(self):
        company = self.request.user.profile.company
        queryset = Profile.objects.filter(company=company).exclude(
            position='Owner')
        return queryset


class CompanyDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAdminUser, SubscribtionIsActive]

    def get_object(self):
        obj = self.request.user.profile
        return obj