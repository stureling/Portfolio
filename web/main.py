from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    pass

@app.route("/search")
def search():
    pass

@app.route("/list")
def listpage():
    pass

@app.route("/projects")
def projects():
    pass

if __name__ == "__main__":
    app.run(debug=True)

