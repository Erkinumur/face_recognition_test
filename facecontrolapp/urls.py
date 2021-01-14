from django.urls import path

from facecontrolapp.views import ImageCompareAPIView

urlpatterns = [
    path('image/compare/', ImageCompareAPIView.as_view())
]
