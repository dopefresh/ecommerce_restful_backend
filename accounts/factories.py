import factory
from factory.django import DjangoModelFactory

from accounts.models import (
    User,
    Employee
)
from shop.factories import CompanyFactory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Faker('random_letters', length=10)
    email = factory.Faker('random_letters', length=15)
    password = factory.Faker('random_letters', length=15)


class EmployeeFactory(DjangoModelFactory):
    class Meta:
        model = Employee
    
    user = factory.SubFactory(UserFactory)
    company = factory.SubFactory(CompanyFactory)

