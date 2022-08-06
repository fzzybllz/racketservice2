from flask import Flask, render_template

# Create a Flask Instance
app = Flask(__name__)

# Route to Home
@app.route("/")
def home():
    return render_template("home.jinja2")

# Error Page
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.jinja2"), 404
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.jinja2"), 500