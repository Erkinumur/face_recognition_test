from django.urls import path

from facecontrolapp.views import ProfileCreateAPIView, ImageCompareAPIView

urlpatterns = [
    path('profile/create/', ProfileCreateAPIView.as_view()),
    path('image/compare/', ImageCompareAPIView.as_view())
]
