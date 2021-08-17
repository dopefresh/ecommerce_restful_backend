from rest_framework import status
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.models import (
    User,
    Employee
)
from accounts.serializers import (
    CreateUserSerializer,
    EmployeeSerializer
)

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from loguru import logger


class SignUpUserView(APIView):
    def get(self, request):
        pass

    @extend_schema(
        description="Register a user",
        tags=["SignUp"],
        request=CreateUserSerializer,
        responses={201: ''}
    )
    def post(self, request):
        user = User.objects.create_user(
            username=request.data.get('username'),
            password=request.data.get('password')
        )
        return Response('', status=status.HTTP_201_CREATED)


class SignUpEmployeeView(APIView): 
    def get(self, request):
        pass

    @extend_schema(
        description="Register an employee",
        tags=["SignUp"],
        request=EmployeeSerializer(many=False),
        responses={201: ''}
    )
    def post(self, request):
        user = User.objects.create_user(
            username=request.data.get('username'),
            password=request.data.get('password')
        )
        Employee.objects.create(
            user=user,
            company=request.data.get('company'),
            phone_number=request.data.get('phone_number')
        )
        return Response('', status=status.HTTP_201_CREATED)
