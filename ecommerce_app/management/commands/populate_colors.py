from django.core.management.base import BaseCommand
from ecommerce_app.models import Color
from webcolors import CSS3_HEX_TO_NAMES

class Command(BaseCommand):
    
    help = 'Populate the Color model with color data'

    def handle(self, *args, **options):

        self.stdout.write(self.style.SUCCESS('Populating Color model...'))

        for hex_code, color_name in CSS3_HEX_TO_NAMES.items():
            # Check if the color already exists in the database to avoid duplicates
            if not Color.objects.filter(color_name=color_name).exists():
                # Create a new Color object and save it to the database
                Color.objects.create(color_name=color_name, color_hex=hex_code)

        self.stdout.write(self.style.SUCCESS('Colors populated successfully!'))
