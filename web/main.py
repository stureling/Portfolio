from flask import Flask, render_template, url_for
import data

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/list")
def listpage():
    return render_template("list.html")

@app.route("/project/<project_id>")
def projects():
    return render_template("project.html", project_id=project_id)

if __name__ == "__main__":
    app.run(debug=True)

