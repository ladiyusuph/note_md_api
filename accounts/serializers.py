from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                username=validated_data.get("username"),
                first_name=validated_data.get("first_name"),
                last_name=validated_data.get("last_name"),
                email=validated_data.get("email"),
                password=validated_data.get("password"),
            )
            return user
        except IntegrityError as e:
            raise serializers.ValidationError(e)
