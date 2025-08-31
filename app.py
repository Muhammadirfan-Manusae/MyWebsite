from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Admin, Content

app = Flask(__name__)
app.secret_key = "mysecret"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


# หน้าแรก
@app.route("/")
def index():
    contents = Content.query.all()
    return render_template("index.html", contents=contents)


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Admin.query.filter_by(username=request.form["username"]).first()
        if user and check_password_hash(user.password, request.form["password"]):
            session["admin"] = user.username
            return redirect(url_for("admin"))
        else:
            flash("Invalid username or password")
    return render_template("login.html")


# Dashboard
@app.route("/admin")
def admin():
    if "admin" not in session:
        return redirect(url_for("login"))
    contents = Content.query.all()
    return render_template("admin.html", contents=contents)


# Add Content
@app.route("/admin/add", methods=["GET", "POST"])
def add_content():
    if "admin" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        new_content = Content(
            title=request.form["title"],
            body=request.form["body"]
        )
        db.session.add(new_content)
        db.session.commit()
        flash("Content added successfully!")
        return redirect(url_for("admin"))
    return render_template("edit_content.html", content=None)


# Edit Content
@app.route("/admin/edit/<int:id>", methods=["GET", "POST"])
def edit_content(id):
    if "admin" not in session:
        return redirect(url_for("login"))
    content = Content.query.get_or_404(id)
    if request.method == "POST":
        content.title = request.form["title"]
        content.body = request.form["body"]
        db.session.commit()
        flash("Content updated successfully!")
        return redirect(url_for("admin"))
    return render_template("edit_content.html", content=content)


# Delete Content
@app.route("/admin/delete/<int:id>")
def delete_content(id):
    if "admin" not in session:
        return redirect(url_for("login"))
    content = Content.query.get_or_404(id)
    db.session.delete(content)
    db.session.commit()
    flash("Content deleted successfully!")
    return redirect(url_for("admin"))


# Logout
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
