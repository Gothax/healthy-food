import os
import django
import sys


sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


import random
from account.models import User
from post.models import Product, Category


def populate_db():
    user = User.objects.create_user(name='testuser2', email='testuser2@example.com', password='testpassword')
    category, created = Category.objects.get_or_create(id=1, name='fruit')

    for i in range(100000):  
        Product.objects.create(
            category=category,
            price=random.randint(50, 150),
            name=f'TestProduct{i}',
            specific='TestSpecific',
            seller=user,
            embeddings=[random.uniform(-1, 1) for _ in range(1536)]
        )
    print("success add")

if __name__ == "__main__":
    populate_db()