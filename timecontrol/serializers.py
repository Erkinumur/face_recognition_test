from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from facecontrolapp.utils import get_face_encoding_string
from .models import TimeControl, Profile, Company, Image

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'file']
        read_only_fields = ['id']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    image = ImageSerializer()

    class Meta:
        model = Profile
        fields = '__all__'


class TimecontrolSerializer(serializers.ModelSerializer):
    # profile = serializers.PrimaryKeyRelatedField(read_only=True)
    profile = ProfileSerializer()

    class Meta:
        model = TimeControl
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']


class ProfileCreateSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()
    company = serializers.SlugRelatedField(slug_field='name',
                                           queryset=Company.objects.all())
    file = serializers.ImageField(source='image.file')

    class Meta:
        model = Profile
        fields = ['user', 'company', 'position', 'file']

    def create(self, validated_data):
        print(validated_data)
        user = validated_data.pop('user')
        image = validated_data.pop('image').get('file')
        password = user.pop('password')
        user = User(**user)
        user.set_password(password)
        user.save()
        profile = Profile.objects.create(user=user, **validated_data)
        encoding = get_face_encoding_string(image)
        Image.objects.create(file=image, encoding=encoding,
                             profile=profile)
        return profile


class CompanySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    company = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = Profile
        exclude = ['position']

