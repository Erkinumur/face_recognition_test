from django.contrib.auth import get_user_model
from rest_framework import serializers

from facecontrolapp.models import Image, Profile
from facecontrolapp.utils import get_face_encoding, get_face_encoding_string

User = get_user_model()


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'file']
        read_only_fields = ['id']


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']


class ProfileCreateSerializer(serializers.ModelSerializer):
    file = serializers.ImageField(source='profile.image.file', required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name',
                  'file']

    def create(self, validated_data):
        print(validated_data)
        image = validated_data.pop('profile').get('image').get('file')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        profile = Profile.objects.create(user=user)
        encoding = get_face_encoding_string(image)
        Image.objects.create(file=image, encoding=encoding,
                             profile=profile)
        return user