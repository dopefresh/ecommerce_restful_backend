from rest_framework import serializers

from accounts.models import User, Employee


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class EmployeeSerializer(serializers.ModelSerializer):
    user = CreateUserSerializer(read_only=False, many=False)

    class Meta:
        model = Employee
        fields = ['phone_number', 'company', 'user']

