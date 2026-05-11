class Product:
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category

    def display_info(self):
        print(f"Nazwa: {self.name}")
        print(f"Cena: {self.price}")
        print(f"""Kategoria: {self.category}
            """)


product1 = Product("Laptop", 2500, "Electronics")
product2 = Product("Smartphone", 1500, "Electronics")
product3 = Product("Table", 300, "Furniture")

product1.display_info()
product2.display_info()
product3.display_info()
