from django.core.management.base import BaseCommand
from ecommerce_app.models import Category, Subcategory

class Command(BaseCommand):
    help = 'Populate categories and subcategories in the database'

    def handle(self, *args, **options):
        # Clear existing categories and subcategories
        Subcategory.objects.all().delete()
        Category.objects.all().delete()

        # Populate categories and subcategories
        categories = [
            {
                'cat_name': 'Books',
                'subcategories': ['Maths', 'Physics', 'Biology', 'Chemistry', 'English', ]
            },
            {
                'cat_name': 'Clothes',
                'subcategories': ['Men', 'Women', 'Kids', 'Top Wear', 'Bottom Wear', 'Winter Wear', 'Foot Wear', 'Inner Wear',]
            },
            {
                'cat_name': 'Home Appliance',
                'subcategories': ['Kitchen Appliances', 'Cleaning Appliances']
            },
            {
                'cat_name': 'Sports and Travel',
                'subcategories': ['Maths', 'Physics', 'Biology', 'Chemistry', 'English', ]
            },
            {
                'cat_name': 'Jwellery',
                'subcategories': ['Men', 'Women', 'Kids', 'Top Wear', 'Bottom Wear', 'Winter Wear', 'Foot Wear', 'Inner Wear',]
            },
            {
                'cat_name': 'Accessories',
                'subcategories': ['Kitchen Appliances', 'Cleaning Appliances']
            },
            {
                'cat_name': 'Automobiles',
                'subcategories': ['Car Models', 'Motorcycles', 'Electric Vehicles', 'Vintage Cars', 'Trucks', 'SUVs', 'Concept Cars']
            },

            {
                'cat_name': 'Musical Items',
                'subcategories': ['Guitar', 'Sitaar', 'Harmonium', 'Mouth Organ', 'Basuri', 'Damroo', 'Dholak', 'Tabla',]
            },
            {
                'cat_name': "Kid's Toyes",
                'subcategories': ['Kitchen Appliances', 'Cleaning Appliances']
            },
            {
                'cat_name': 'Smartphones',
                'subcategories': ['Maths', 'Physics', 'Biology', 'Chemistry', 'English', ]
            },
            {
                'cat_name': 'Keypad Phones',
                'subcategories': ['Nokia', 'Kechoda', 'Intex', 'Samsung', 'Gionee', 'Micromax', '', 'Inner Wear',]
            },
            {
                'cat_name': "Pet Items",
                'subcategories': ['Kitchen Appliances', 'Cleaning Appliances']
            },
           
        ]

        for category_data in categories:
            category_name = category_data['cat_name']
            subcategories = category_data['subcategories']

            category = Category.objects.create(cat_name=category_name)

            for subcategory_name in subcategories:
                Subcategory.objects.create(sub_cat_name=subcategory_name, category=category)

        self.stdout.write(self.style.SUCCESS('Categories and subcategories populated successfully.'))
