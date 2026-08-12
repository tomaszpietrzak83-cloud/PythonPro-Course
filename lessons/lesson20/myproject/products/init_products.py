# --- TASK 04 ---
# --- TASK 09 ---
from decimal import Decimal

from .models import Category, Product


def init_products():
    products = [
        {
            "name": "Laptop",
            "price": "999.99",
            "description": "A high-performance laptop.",
            "category": "Electronics",
        },
        {
            "name": "Smartphone",
            "price": "499.99",
            "description": "A sleek and powerful smartphone.",
            "category": "Electronics",
        },
        {
            "name": "Headphones",
            "price": "199.99",
            "description": "Noise-cancelling over-ear headphones.",
            "category": "Electronics",
        },
        {
            "name": "Coffee Maker",
            "price": "79.99",
            "description": "Brew the perfect cup of coffee.",
            "category": "Home & Kitchen",
        },
        {
            "name": "Running Shoes",
            "price": "129.99",
            "description": "Comfortable and durable running shoes.",
            "category": "Sports & Outdoors",
        },
        {
            "name": "Electric Toothbrush",
            "price": "59.99",
            "description": "Keep your teeth clean and healthy.",
            "category": "Health & Personal Care",
        },
        {
            "name": "Gaming Console",
            "price": "399.99",
            "description": "Experience next-gen gaming.",
            "category": "Electronics",
        },
        {
            "name": "Blender",
            "price": "89.99",
            "description": "Make smoothies and more with ease.",
            "category": "Home & Kitchen",
        },
        {
            "name": "Action Figure",
            "price": "24.99",
            "description": "Collectible action figure for fans.",
            "category": "Toys & Games",
        },
        {
            "name": "Cookbook",
            "price": "29.99",
            "description": "Discover new recipes and cooking techniques.",
            "category": "Books",
        },
        {
            "name": "Yoga Mat",
            "price": "29.99",
            "description": "Non-slip yoga mat for a comfortable practice.",
            "category": "Sports & Outdoors",
        },
        {
            "name": "Car Vacuum Cleaner",
            "price": "49.99",
            "description": "Keep your car clean and fresh.",
            "category": "Automotive",
        },
        {
            "name": "Wireless Mouse",
            "price": "29.99",
            "description": "A smooth and reliable wireless mouse for daily use.",
            "category": "Electronics",
        },
        {
            "name": "Bluetooth Speaker",
            "price": "89.99",
            "description": "Portable speaker with clear sound and deep bass.",
            "category": "Electronics",
        },
        {
            "name": "Tablet Stand",
            "price": "24.99",
            "description": "Adjustable stand for tablets and e-readers.",
            "category": "Electronics",
        },
        {
            "name": "USB-C Hub",
            "price": "39.99",
            "description": "Expand your laptop with multiple useful ports.",
            "category": "Electronics",
        },
        {
            "name": "Smartwatch",
            "price": "199.99",
            "description": "Track fitness, notifications, and daily activity.",
            "category": "Electronics",
        },
        {
            "name": "Winter Jacket",
            "price": "149.99",
            "description": "Warm and stylish jacket for cold weather.",
            "category": "Clothing",
        },
        {
            "name": "Cotton T-Shirt",
            "price": "19.99",
            "description": "Soft cotton t-shirt for everyday comfort.",
            "category": "Clothing",
        },
        {
            "name": "Running Shorts",
            "price": "34.99",
            "description": "Lightweight shorts designed for active movement.",
            "category": "Clothing",
        },
        {
            "name": "Leather Belt",
            "price": "44.99",
            "description": "Classic belt made from durable leather.",
            "category": "Clothing",
        },
        {
            "name": "Wool Scarf",
            "price": "27.99",
            "description": "Cozy scarf to keep you warm in winter.",
            "category": "Clothing",
        },
        {
            "name": "Air Fryer",
            "price": "129.99",
            "description": "Cook crispy meals with less oil.",
            "category": "Home & Kitchen",
        },
        {
            "name": "Ceramic Dinner Set",
            "price": "74.99",
            "description": "Elegant dinnerware set for family meals.",
            "category": "Home & Kitchen",
        },
        {
            "name": "Bedside Lamp",
            "price": "39.99",
            "description": "Soft lighting lamp perfect for bedrooms.",
            "category": "Home & Kitchen",
        },
        {
            "name": "Kitchen Knife Set",
            "price": "59.99",
            "description": "Sharp and practical knives for cooking.",
            "category": "Home & Kitchen",
        },
        {
            "name": "Storage Basket",
            "price": "22.99",
            "description": "Keep your home tidy with this woven basket.",
            "category": "Home & Kitchen",
        },
        {
            "name": "Mystery Novel",
            "price": "14.99",
            "description": "A suspenseful story full of twists and secrets.",
            "category": "Books",
        },
        {
            "name": "Python Basics Guide",
            "price": "34.99",
            "description": "A beginner-friendly book for learning Python.",
            "category": "Books",
        },
        {
            "name": "Healthy Recipes Book",
            "price": "24.99",
            "description": "A collection of fresh and nutritious meals.",
            "category": "Books",
        },
        {
            "name": "Travel Photography Book",
            "price": "29.99",
            "description": "Inspiring photos and tips for travelers.",
            "category": "Books",
        },
        {
            "name": "Mindfulness Journal",
            "price": "17.99",
            "description": "A guided journal for reflection and calm.",
            "category": "Books",
        },
        {
            "name": "Puzzle Board Game",
            "price": "34.99",
            "description": "A fun game night challenge for the family.",
            "category": "Toys & Games",
        },
        {
            "name": "Remote Control Car",
            "price": "54.99",
            "description": "Fast and exciting toy car with remote control.",
            "category": "Toys & Games",
        },
        {
            "name": "Building Blocks Set",
            "price": "39.99",
            "description": "Creative construction set for kids and adults.",
            "category": "Toys & Games",
        },
        {
            "name": "Plush Teddy Bear",
            "price": "18.99",
            "description": "Soft teddy bear perfect for gifts and cuddles.",
            "category": "Toys & Games",
        },
        {
            "name": "Science Experiment Kit",
            "price": "46.99",
            "description": "Educational kit packed with fun experiments.",
            "category": "Toys & Games",
        },
        {
            "name": "Camping Lantern",
            "price": "32.99",
            "description": "Bright and durable lantern for outdoor trips.",
            "category": "Sports & Outdoors",
        },
        {
            "name": "Resistance Bands",
            "price": "21.99",
            "description": "Versatile bands for home workouts and stretching.",
            "category": "Sports & Outdoors",
        },
        {
            "name": "Tennis Racket",
            "price": "89.99",
            "description": "Lightweight racket for practice and matches.",
            "category": "Sports & Outdoors",
        },
        {
            "name": "Insulated Water Bottle",
            "price": "26.99",
            "description": "Keeps drinks cold or hot for hours.",
            "category": "Sports & Outdoors",
        },
        {
            "name": "Hiking Backpack",
            "price": "79.99",
            "description": "Spacious backpack for hiking and travel.",
            "category": "Sports & Outdoors",
        },
        {
            "name": "Vitamin C Serum",
            "price": "19.99",
            "description": "Brighten and refresh your skin daily.",
            "category": "Beauty",
        },
        {
            "name": "Hair Dryer",
            "price": "49.99",
            "description": "Quick-drying hair tool with multiple settings.",
            "category": "Beauty",
        },
        {
            "name": "Nail Care Set",
            "price": "16.99",
            "description": "Complete set for clean and neat nails.",
            "category": "Beauty",
        },
        {
            "name": "Aloe Vera Gel",
            "price": "12.99",
            "description": "Soothing gel for skin hydration and care.",
            "category": "Beauty",
        },
        {
            "name": "Makeup Brush Set",
            "price": "27.99",
            "description": "A soft brush collection for smooth makeup application.",
            "category": "Beauty",
        },
        {
            "name": "First Aid Kit",
            "price": "24.99",
            "description": "Essential medical supplies for home and travel.",
            "category": "Health & Personal Care",
        },
        {
            "name": "Digital Thermometer",
            "price": "14.99",
            "description": "Accurate thermometer for quick temperature checks.",
            "category": "Health & Personal Care",
        },
        {
            "name": "Massage Gun",
            "price": "89.99",
            "description": "Relax sore muscles with deep tissue massage.",
            "category": "Health & Personal Care",
        },
        {
            "name": "Multivitamin Pack",
            "price": "18.99",
            "description": "Daily vitamins to support overall wellness.",
            "category": "Health & Personal Care",
        },
        {
            "name": "Toothpaste Set",
            "price": "11.99",
            "description": "Fresh and effective toothpaste for daily care.",
            "category": "Health & Personal Care",
        },
        {
            "name": "Windshield Sun Shade",
            "price": "19.99",
            "description": "Protect your car interior from heat and sunlight.",
            "category": "Automotive",
        },
        {
            "name": "Car Phone Mount",
            "price": "17.99",
            "description": "Securely hold your phone while driving.",
            "category": "Automotive",
        },
        {
            "name": "Tire Pressure Gauge",
            "price": "13.99",
            "description": "Check tire pressure quickly and accurately.",
            "category": "Automotive",
        },
        {
            "name": "Seat Organizer",
            "price": "23.99",
            "description": "Keep your car essentials organized and within reach.",
            "category": "Automotive",
        },
        {
            "name": "Emergency Road Kit",
            "price": "59.99",
            "description": "Prepared kit for unexpected roadside situations.",
            "category": "Automotive",
        },
        {
            "name": "Organic Oatmeal",
            "price": "7.99",
            "description": "Healthy whole grain breakfast option.",
            "category": "Grocery",
        },
        {
            "name": "Dark Roast Coffee Beans",
            "price": "15.99",
            "description": "Rich and bold coffee for every morning.",
            "category": "Grocery",
        },
        {
            "name": "Olive Oil Bottle",
            "price": "12.99",
            "description": "Premium olive oil for cooking and salads.",
            "category": "Grocery",
        },
        {
            "name": "Green Tea Pack",
            "price": "9.99",
            "description": "Refreshing tea with a clean natural taste.",
            "category": "Grocery",
        },
        {
            "name": "Mixed Nuts Jar",
            "price": "14.99",
            "description": "Crunchy snack mix full of energy and flavor.",
            "category": "Grocery",
        },
    ]

    for product_data in products:
        category_name = product_data.get("category")
        category = None

        if category_name:
            category, _ = Category.objects.get_or_create(name=category_name)
        product, created = Product.objects.get_or_create(
            name=product_data["name"],
            defaults={
                "price": Decimal(product_data["price"]),
                "description": product_data["description"],
                "category": category,
            },
        )

        if created:
            print(f"Added: {product.name}")
        else:
            print(f"Already exists: {product.name}")

        if not created:
            updated = False

            if product.price != Decimal(product_data["price"]):
                product.price = Decimal(product_data["price"])
                updated = True

            if product.description != product_data["description"]:
                product.description = product_data["description"]
                updated = True

            if product.category != category:
                product.category = category
                updated = True

            if updated:
                product.save()
                print(f"Updated: {product.name}")
            else:
                print(f"Already exists: {product.name}")
        else:
            print(f"Added: {product.name}")
