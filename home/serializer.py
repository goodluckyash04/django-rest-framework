from django.contrib.auth.models import User
from rest_framework import serializers
import re

from .models import Person, Color


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user_name = data.get("username")
        email = data.get("email")
        if user_name:
            if User.objects.filter(username=user_name).exists():
                raise serializers.ValidationError("Username Already exist")
        if email:
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError("Email Already exist")
        return data

    def create(self, validated_data):
        print(validated_data.get("username"))
        new_user = User.objects.create(
            username=validated_data.get("username"), email=validated_data.get("email")
        )
        new_user.set_password(validated_data["password"])
        new_user.save()
        return validated_data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = "__all__"


class PeopleSerializer(serializers.ModelSerializer):
    fav_color = ColorSerializer()
    country = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = "__all__"
        # fields = ["person_name"]
        # exclude = ["age"]
        # depth = 1  # gives complete object

    def get_country(self, obj):
        obj = Color.objects.get(color_name=obj.fav_color.color_name)
        return {"col_name": obj.color_hash}

    def validate_person_name(self, person_name):
        if not re.match(r"^[A-Za-z\s'-]+$", person_name):
            raise serializers.ValidationError("Name must not have special char")
        return person_name

    def validate(self, data):
        if data["age"] not in range(18, 100):
            raise serializers.ValidationError("age must be between 18 to 100")
        return data
