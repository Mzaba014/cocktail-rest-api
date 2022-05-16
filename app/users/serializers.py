from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User objects"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, data):
        """Use data from HTTP post to create new User"""
        return get_user_model().objects.create_user(**data)

    def update(self, instance, data):
        """Updates the user data and sets their password using the hashing helper method"""
        password = data.pop('password', None)  # remove password from the data set
        user = super().update(instance, data)  # update all attributes besides the password

        # set password using helper method if password is not None
        if password is not None:
            user.set_password(password)
            user.save()

        # return the updated user
        return user


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attributes):
        email = attributes.get('email')
        password = attributes.get('password')

        # makes a call and returns a User object if the creds are valid
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        # raise authentication exception if user is not valid
        if user is None:
            message = 'Could not authenticate with the credentials provided'
            raise serializers.ValidationError(message, code='authentication')

        # return the modified attributes post-verification
        attributes['user'] = user
        return attributes
