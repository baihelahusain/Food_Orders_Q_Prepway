import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodsite.settings')
django.setup()

# Import models
from food.models import Item

# Sample food items with categories
def add_sample_data():
    print("Adding sample food items...")
    
    # Fast Food category
    Item.objects.create(
        Item_name="French Fries",
        Item_desc="Crispy golden fries served with ketchup and mayo.",
        Item_price=99,
        Item_img="https://images.unsplash.com/photo-1630384060421-8035617be2e3?q=80&w=1000",
        category="fast_food",
        prep_time="15 minutes"
    )
    
    Item.objects.create(
        Item_name="Chicken Nuggets",
        Item_desc="Crispy chicken nuggets served with dipping sauce.",
        Item_price=149,
        Item_img="https://images.unsplash.com/photo-1562967914-608f82629710",
        category="fast_food",
        prep_time="10 minutes"
    )
    
    Item.objects.create(
        Item_name="Margherita Pizza",
        Item_desc="Classic Italian pizza with tomato sauce, mozzarella, and fresh basil.",
        Item_price=249,
        Item_img="https://images.unsplash.com/photo-1574071318508-1cdbab80d002",
        category="fast_food",
        prep_time="25 minutes"
    )
    
    Item.objects.create(
        Item_name="Classic Burger",
        Item_desc="Juicy beef patty with lettuce, tomato, and cheese in a soft bun.",
        Item_price=199,
        Item_img="https://images.unsplash.com/photo-1568901346375-23c9450c58cd",
        category="fast_food",
        prep_time="20 minutes"
    )
    
    # Main Course category
    Item.objects.create(
        Item_name="Chicken Biryani",
        Item_desc="Fragrant basmati rice cooked with tender chicken pieces and aromatic spices.",
        Item_price=249,
        Item_img="https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8",
        category="main_course",
        prep_time="40 minutes"
    )
    
    Item.objects.create(
        Item_name="Veg Biryani",
        Item_desc="Flavorful rice dish made with mixed vegetables and fragrant spices.",
        Item_price=199,
        Item_img="https://media.istockphoto.com/id/1345624336/photo/veg-biryani.jpg",
        category="main_course",
        prep_time="35 minutes"
    )
    
    Item.objects.create(
        Item_name="Butter Chicken",
        Item_desc="Tender chicken pieces in a rich, creamy tomato-based sauce.",
        Item_price=299,
        Item_img="https://images.unsplash.com/photo-1603894584373-5ac82b2ae398",
        category="main_course",
        prep_time="45 minutes"
    )
    
    Item.objects.create(
        Item_name="Paneer Tikka Masala",
        Item_desc="Grilled cottage cheese cubes in a spiced creamy tomato sauce.",
        Item_price=249,
        Item_img="https://media.istockphoto.com/id/967311428/photo/indian-cuisine-kadai-paneer-curry-dish.jpg",
        category="main_course",
        prep_time="30 minutes"
    )
    
    # Drinks category
    Item.objects.create(
        Item_name="Mango Lassi",
        Item_desc="Refreshing yogurt-based drink with sweet mango pulp.",
        Item_price=89,
        Item_img="https://images.unsplash.com/photo-1553530979-3b15ce94b0e6",
        category="drinks",
        prep_time="5 minutes"
    )
    
    Item.objects.create(
        Item_name="Masala Chai",
        Item_desc="Traditional Indian spiced tea with milk.",
        Item_price=49,
        Item_img="https://images.unsplash.com/photo-1561336313-0bd5e0b27ec8",
        category="drinks",
        prep_time="10 minutes"
    )
    
    # Sweet category
    Item.objects.create(
        Item_name="Gulab Jamun",
        Item_desc="Soft, spongy milk-solid-based sweet soaked in sugar syrup.",
        Item_price=99,
        Item_img="https://media.istockphoto.com/id/1156896083/photo/gulab-jamun-sugar-syrup-and-dry-fruits-indian-sweet.jpg",
        category="sweet",
        prep_time="25 minutes"
    )
    
    Item.objects.create(
        Item_name="Chocolate Brownie",
        Item_desc="Rich, fudgy chocolate brownie served with vanilla ice cream.",
        Item_price=149,
        Item_img="https://images.unsplash.com/photo-1606313564200-e75d5e30476c",
        category="sweet",
        prep_time="30 minutes"
    )
    
    print(f"Added {Item.objects.count()} food items")

if __name__ == "__main__":
    add_sample_data() 