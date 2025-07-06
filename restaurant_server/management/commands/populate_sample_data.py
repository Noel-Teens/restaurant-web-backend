from django.core.management.base import BaseCommand
from restaurant_server.models import MenuItem


class Command(BaseCommand):
    help = 'Populate the database with sample menu items'

    def handle(self, *args, **options):
        # Sample menu items
        sample_items = [
            {
                'food_name': 'Margherita Pizza',
                'food_description': 'Classic pizza with fresh tomatoes, mozzarella, and basil',
                'food_price': 12.99
            },
            {
                'food_name': 'Caesar Salad',
                'food_description': 'Crisp romaine lettuce with parmesan cheese and croutons',
                'food_price': 8.99
            },
            {
                'food_name': 'Grilled Salmon',
                'food_description': 'Fresh Atlantic salmon grilled to perfection with herbs',
                'food_price': 18.99
            },
            {
                'food_name': 'Chicken Alfredo',
                'food_description': 'Creamy pasta with grilled chicken and parmesan cheese',
                'food_price': 15.99
            },
            {
                'food_name': 'Chocolate Cake',
                'food_description': 'Rich chocolate cake with chocolate frosting',
                'food_price': 6.99
            },
            {
                'food_name': 'Beef Burger',
                'food_description': 'Juicy beef patty with lettuce, tomato, and cheese',
                'food_price': 11.99
            },
            {
                'food_name': 'Vegetable Stir Fry',
                'food_description': 'Fresh mixed vegetables stir-fried with soy sauce',
                'food_price': 10.99
            },
            {
                'food_name': 'Fish Tacos',
                'food_description': 'Grilled fish with cabbage slaw in soft tortillas',
                'food_price': 13.99
            }
        ]

        created_count = 0
        for item_data in sample_items:
            menu_item, created = MenuItem.objects.get_or_create(
                food_name=item_data['food_name'],
                defaults=item_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created menu item: {menu_item.food_name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Menu item already exists: {menu_item.food_name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new menu items')
        )
