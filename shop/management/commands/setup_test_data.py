import random

from django.db import transaction
from django.core.management.base import BaseCommand

from accounts.models import (
    User,
    Employee
)

from accounts.factories import (
    UserFactory,
    EmployeeFactory
)

from shop.models import (
    Company,
    Category,
    SubCategory,
    Item
)
from shop.factories import (
    CompanyFactory,
    CategoryFactory,
    SubCategoryFactory,
    ItemFactory
)

from loguru import logger

USERS = 5000
EMPLOYEES = 3000
COMPANIES = 100
CATEGORIES = 100
SUBCATEGORIES = 2000
ITEMS=5000


class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic(using='test')
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        models = [User, Employee, Company, Category, SubCategory, Item]
        for m in models:
            m.objects.all().delete()

        # Create all the users
        self.stdout.write("Creating users")
        people = []
        for _ in range(USERS):
            person = UserFactory()
            people.append(person)
        
        # Create all the companies
        self.stdout.write("Creating companies")
        all_companies = []
        for _ in range(COMPANIES):
            comp = CompanyFactory()
            all_companies.append(comp)

        # Create all the employees
        all_employees = []
        self.stdout.write("Creating employees")
        for _ in range(EMPLOYEES):
            random_company = random.choice(all_companies)
            emp = EmployeeFactory(company=random_company)
            all_employees.append(emp)
        
        self.stdout.write("Creating categories")
        # Create all the categories
        all_categories = []
        for _ in range(CATEGORIES):
            categ = CategoryFactory()
            all_categories.append(categ)

        # Create all the sub categories
        self.stdout.write("Creating sub categories")
        all_subcategories = []
        for _ in range(SUBCATEGORIES):
            random_category = random.choice(all_categories)
            subcateg = SubCategoryFactory(category=random_category)
            all_subcategories.append(subcateg)
        
        # Create all the items
        self.stdout.write("Creating items")
        all_items = []
        for _ in range(ITEMS):
            random_subcategory = random.choice(all_subcategories)
            random_company = random.choice(all_companies)
            new_item = ItemFactory(company=random_company, sub_category=random_subcategory)





