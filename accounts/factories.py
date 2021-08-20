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
    
    username = factory.Faker('pystr', max_chars=20, min_chars=12)
    email = factory.Faker('pystr', max_chars=20, min_chars=12)
    password = factory.Faker('pystr', max_chars=20, min_chars=12)
    
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        # The default would use ``manager.create(*args, **kwargs)``
        return manager.create_user(*args, **kwargs)

class EmployeeFactory(DjangoModelFactory):
    class Meta:
        model = Employee
    
    user = factory.SubFactory(UserFactory)
    company = factory.SubFactory(CompanyFactory)
    phone_number = factory.Faker('phone_number')
