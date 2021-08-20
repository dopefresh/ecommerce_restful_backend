import factory
from factory.django import DjangoModelFactory

from shop.models import (
    Company,
    Category,
    SubCategory,
    Item
)


class CompanyFactory(DjangoModelFactory):
    class Meta:
        model = Company
    
    name = factory.Faker('pystr', min_chars=12, max_chars=20)
    location = factory.Faker('address')
    phone_number = factory.Faker('phone_number')


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category
    
    title = factory.Faker('pystr', min_chars=12, max_chars=20)


class SubCategoryFactory(DjangoModelFactory):
    class Meta:
        model = SubCategory
    
    category = factory.SubFactory(CategoryFactory)
    title = factory.Faker('pystr', min_chars=12, max_chars=20)


class ItemFactory(DjangoModelFactory):
    class Meta:
        model = Item
    
    title = factory.Faker('pystr', min_chars=20, max_chars=30)
    description = factory.Faker('sentence', nb_words=20)
    price = factory.Faker('random_int')
    sub_category = factory.SubFactory(SubCategoryFactory)
    company = factory.SubFactory(CompanyFactory)

