from database import SessionLocal, engine
from flask import Flask, render_template
from models import Base, Product

db = SessionLocal()

app = Flask(__name__)
Base.metadata.create_all(bind=engine)


@app.route("/index")
@app.route("/")
def index():
    return render_template("index.html", title="Lesson 17 App")


# TASK 01
@app.route("/me")
def me():
    return render_template(
        "simple_result.html",
        title="About Me",
        heading="About Me",
        message="Tomasz Pietrzak",
    )


# TASK 02
@app.route("/<function_name>/<int:a>/<int:b>")
def function(function_name, a, b):
    if function_name == "add":
        result = a + b
    elif function_name == "subtract":
        result = a - b
    else:
        return render_template(
            "simple_result.html",
            title="Invalid function",
            heading="Invalid function",
            message="Use 'add' or 'subtract'. Example: /add/5/3 or /subtract/10/4",
        )

    return render_template(
        "simple_result.html",
        title="Calculator Result",
        heading="Calculator Result",
        message=f"{function_name}({a}, {b}) = {result}",
    )


# TASK 03, 04
@app.route("/movies")
def movies():
    movies_list = ["Inception", "The Matrix", "Interstellar", "The Dark Knight"]
    title = "My favorite movies"
    return render_template("movies.html", movies=movies_list, title=title)


# TASK 06
@app.route("/book")
def book():
    book_items = {
        "title": "Ender's Game",
        "author": "Orson Scott Card",
        "year": 1985,
        "genre": "Science Fiction",
    }
    return render_template(
        "book.html",
        title=book_items["title"],
        author=book_items["author"],
        year=book_items["year"],
        genre=book_items["genre"],
    )


# TASK 07
@app.route("/gallery")
def gallery():
    images = [
        {
            "url": "https://thumbs.dreamstime.com/b/environment-earth-day-hands-trees-growing-seedlings-bokeh-green-background-female-hand-holding-tree-nature-field-gra-130247647.jpg?w=992",
            "caption": "Earth Day",
        },
        {
            "url": "https://thumbs.dreamstime.com/b/mont-blanc-9130539.jpg?w=768",
            "caption": "Mont Blanc",
        },
        {
            "url": "https://thumbs.dreamstime.com/b/autumn-nature-landscape-colorful-forest-autumn-nature-landscape-colorful-forest-morning-sunlight-131400332.jpg?w=992",
            "caption": "Autumn Forest",
        },
        {
            "url": "https://thumbs.dreamstime.com/b/orange-yellow-sunset-sky-water-mirror-nature-landscape-beautiful-clouds-sun-burst-rays-above-light-reflection-lake-159927963.jpg?w=768",
            "caption": "Sunset Reflection",
        },
        {
            "url": "https://thumbs.dreamstime.com/b/beautiful-sunset-over-water-tree-silhouette-nature-landscape-amazing-orange-yellow-sky-night-scene-wallpaper-birds-flying-154424473.jpg?w=768",
            "caption": "Sunset Silhouette",
        },
        {
            "url": "https://thumbs.dreamstime.com/b/landscape-nature-mountan-alps-rainbow-76824355.jpg?w=768",
            "caption": "Mountain Rainbow",
        },
    ]
    title = "Nature Gallery"
    return render_template("gallery.html", images=images, title=title)


# TASK 09
@app.route("/products")
def products():
    title = "Products List"
    products_list = db.query(Product).all()
    return render_template("products.html", products=products_list, title=title)


if __name__ == "__main__":
    app.run(debug=True)
