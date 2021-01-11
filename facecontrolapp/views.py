from rest_framework import generics, views, status
from rest_framework.response import Response

from facecontrolapp.models import Profile, Image
from facecontrolapp.serializers import ProfileCreateSerializer, \
    ImageSerializer
from facecontrolapp.utils import get_face_encoding, face_compare


class ProfileCreateAPIView(generics.CreateAPIView):
    model = Profile
    serializer_class = ProfileCreateSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        return super().create(request, *args, **kwargs)


class ImageCompareAPIView(views.APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = ImageSerializer(data=request.data, context={'request':
                                                                     request})
        serializer.is_valid(raise_exception=True)
        image = serializer.validated_data.get('file')
        unknown_face = get_face_encoding(image)
        try:
            unknown_face[0]
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            queryset = Image.objects.all()
            result: Image = face_compare(unknown_face, queryset)
            if result:
                img_serializer = ImageSerializer(
                    result,
                    context={'request': request})
                data = img_serializer.data
                return Response(data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_204_NO_CONTENT)