from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class UserSerializer(serializers.ModelSerializer):

    username = serializers.RegexField(
        required=True,
        max_length=150,
        regex=r"^[^\W\d]\w*$",
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    email = serializers.EmailField(
        required=True,
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role'
        )
        model = User
        read_only_field = ('role',)
