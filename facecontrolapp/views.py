from rest_framework import views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from facecontrolapp.utils import get_face_encoding, face_compare
from timecontrol.models import Image
from timecontrol.permissions import SubscribtionIsActive
from timecontrol.serializers import ImageSerializer, ProfileSerializer


class ImageCompareAPIView(views.APIView):
    permission_classes = [IsAuthenticated, SubscribtionIsActive]

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = ImageSerializer(data=request.data,
                                     context={'request': request})
        serializer.is_valid(raise_exception=True)
        image = serializer.validated_data.get('file')
        unknown_face = get_face_encoding(image)
        try:
            unknown_face[0]
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            company = request.user.profile.company
            queryset = Image.objects.filter(
                profile__company=company).select_related('profile')
            result: Image = face_compare(unknown_face, queryset)
            if result:
                profile = result.profile
                profile_serializer = ProfileSerializer(
                    profile, context={'request': request}
                )
                # img_serializer = ImageSerializer(
                #     result,
                #     context={'request': request})
                data = profile_serializer.data
                return Response(data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_204_NO_CONTENT)