import inspect

from exercises.ex01 import count_products
from exercises.ex02 import find_max_price
from exercises.ex03 import sum_all_in_electronics
from exercises.ex04 import average_price_in_books
from exercises.ex05 import display_customers_name_and_email
from exercises.ex06 import show_all_products_above_average
from exercises.ex07 import show_specific_customer_order
from exercises.ex08 import count_products_in_all_categories
from exercises.ex09 import find_all_electronics_products
from exercises.ex10 import convert_products_to_objects
from flask import Flask, render_template
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

app = Flask(__name__)

exercises = {
    1: {
        "name": "Product counter",
        "func": count_products,
        "result_text": "Total number of products:",
    },
    2: {
        "name": "Maximum price finder",
        "func": find_max_price,
        "result_text": "The highest product price is: ",
    },
    3: {
        "name": "Summarize prices in electronics",
        "func": sum_all_in_electronics,
        "result_text": "The total value of products in the Electronics category is:",
    },
    4: {
        "name": "Counts average price in books",
        "func": average_price_in_books,
        "result_text": "The average price in books category is:",
    },
    5: {
        "name": "Displays customer data",
        "func": display_customers_name_and_email,
        "result_text": "Customer names and emails are:",
    },
    6: {
        "name": "Displays all products data above average",
        "func": show_all_products_above_average,
        "result_text": "Products names and prices are:",
    },
    7: {
        "name": "Shows specific customer order items",
        "func": show_specific_customer_order,
        "result_text": "Order contains:",
    },
    8: {
        "name": "Shows number of items in categories",
        "func": count_products_in_all_categories,
        "result_text": "Number of items per category:",
    },
    9: {
        "name": "Displays all electronic products",
        "func": find_all_electronics_products,
        "result_text": "Products names and prices are:",
    },
    10: {
        "name": "Converts all products to objects",
        "func": convert_products_to_objects,
        "result_text": "Products:",
    },
}


@app.route("/")
def index():
    return render_template("index.html", exercises=exercises)


@app.route("/task/<int:id>")
def task(id):
    task = exercises[id]
    code = inspect.getsource(exercises[id]["func"])
    html_code = highlight(code, PythonLexer(), HtmlFormatter())
    result = task["func"]()

    return render_template(
        "task.html", task=task, code=html_code, result=result
    )


if __name__ == "__main__":
    app.run(debug=True)
