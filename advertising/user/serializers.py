from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.generics import get_object_or_404
from django.contrib.auth.hashers import check_password
from user.models import User



class LoginSerializer(AuthTokenSerializer):

    def update(self, instance, validated_data):
        raise NotImplementedError

    def create(self, validated_data):
        raise NotImplementedError

    def validate(self, data):
        email, password = data.get('username', ''), data.get('password', '')
        print(email, password)
        user = get_object_or_404(User.objects.all(), email=email)

        if not check_password(password, user.password):
            raise ValidationError(
                '~WRONG PASSWORD~', code=HTTP_403_FORBIDDEN
            )

        data['user'] = user
        return data
