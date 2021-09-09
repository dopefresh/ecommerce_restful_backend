from rest_framework import status
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

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


@api_view(['POST'])
def check_username_exists_view(request):
    username = request.data.get('username')
    user_query = User.objects.filter(username=username)
    if user_query.exists():
        return Response({'exists': True}, status=status.HTTP_200_OK)
    return Response({'exists': False}, status=status.HTTP_200_OK)


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
        try:
            logger.info("Going to create a user")
            user = User.objects.create_user(
                username=request.data.get('username'),
                email=request.data.get('email'),
                password=request.data.get('password'),
                role='user'
            )
            return Response('', status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(e)
            return Response('', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
            password=request.data.get('password'),
            role='employee'
        )
        Employee.objects.create(
            user=user,
            company=request.data.get('company'),
            phone_number=request.data.get('phone_number')
        )
        return Response('', status=status.HTTP_201_CREATED)
