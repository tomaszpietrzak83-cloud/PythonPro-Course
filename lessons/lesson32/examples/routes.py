"""Routing for task19; handlers are supplied explicitly to avoid circular imports."""

def setup_routes(app, create_product, list_products, get_product):
    app.router.add_post("/products", create_product)
    app.router.add_get("/products", list_products)
    app.router.add_get("/products/{id}", get_product)
