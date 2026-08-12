from database import SessionLocal
from flask import Flask, render_template, request, redirect, url_for
from models import Registry

db = SessionLocal()

app = Flask(__name__)


@app.route("/index")
def index():
    title = "Registry App"
    return render_template("index.html", title=title)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")

        new_registry = Registry()
        result = new_registry.add_registry(db, name=name, email=email)

        if isinstance(result, str):
            return result
        return redirect(url_for("ty"))
    return render_template("registration.html", title="Registry App")


@app.route("/ty")
def ty():
    title = "Registration Successful"
    return render_template("ty.html", title=title)


if __name__ == "__main__":
    app.run(debug=True)
