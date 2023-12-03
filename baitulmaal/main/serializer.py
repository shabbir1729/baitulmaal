from .models import *
from rest_framework import serializers
import re

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'first_name', 'last_name', 'username',
         'password', 'email','address', 'phone')
        # fields = '__all__' 
        model = User
        extra_kwargs = {'password': {'write_only': True}}


    def validate_password(self, password):
        if len(password) < 8:
            raise serializers.ValidationError("The password must contain at least 8 characters")
        if not re.findall('\d', password):
            raise serializers.ValidationError("The password must contain at least 1 digit, 0-9.")
        if not re.findall('[A-Z]', password):
            raise serializers.ValidationError("The password must contain at least 1 uppercase letter, A-Z.")
        if not re.findall('[a-z]', password):
            raise serializers.ValidationError("The password must contain at least 1 lowercase letter, a-z.")
        if not re.findall('[!@#$%^&*()]', password):
            raise serializers.ValidationError("The password must contain at least 1 symbol: " + "!@#$%^&*()")
        return password


    def create(self, validated_data):

        if validated_data:

            user = User.objects.create(**validated_data)
            user.set_password(validated_data['password'])
            user.save()
            return user
        else:
            raise serializers.ValidationError


class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Members
        fields = "__all__"


class ContributionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contribution
        fields = "__all__"


class LoanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Loan
        fields = "__all__"


