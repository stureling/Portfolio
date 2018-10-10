from flask import Flask, render_template, url_for, request, redirect
from flask import session, abort, flash, escape
import data
import os
from flask_login import LoginManager, login_user, login_required, UserMixin
from flask_login import logout_user

# Start Flask
app = Flask(__name__)
app.secret_key = os.urandom(64)
db = data.load("data.json")


# User class for Flask-Login
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

# Database file of all the users and their passwords
users = data.load_users("users.json")

# Start Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


# Start Flask routes
@app.route("/bootstrap")
def bootstrap():
    projects = data.search(db, search="")
    return render_template("index_bootstrap2.html", **locals())

@app.route("/")
def index():
    return render_template("index.html", database=db)

@app.route("/techniques")
def techniques():
    """Creates and sorts a list of all project by the technique used.
    Then it displays a page of all projects"""
    master_list = []
    technique_list = data.get_techniques(db)
    for e in technique_list:
        temp_list = [e]
        temp_list.append(data.search(db, techniques=[e]))
        master_list.append(temp_list)
    for i in master_list:
        if len(i[1]) > len(master_list[0][1]):
            new_pos = master_list.pop(master_list.index(i))
            master_list.insert(0, new_pos)
    return render_template("techniques.html", master_list=master_list)

@app.route("/list", methods=["POST", "GET"])
def list():
    """Creates a page where you can search the database
    for projects and sort them"""
    technique_data = data.get_techniques(db)
    search_fields = data.get_searchfields(db)

    if request.method == "POST":
        search = request.form["search"]
        techniques = request.form.getlist("techniques")
        searched_fields = request.form.getlist("searched_fields")
        requested_projects = data.search(db, search=search,
                                         search_fields=searched_fields,
                                         techniques=techniques)
        return render_template("list_bootstrap.html",**locals())
    else:
        return render_template("list_bootstrap.html", **locals())

@app.route("/project/<project_id>")
def project(project_id):
    if data.get_project(db, int(project_id)):
        return render_template("project.html",
                           project=data.get_project(db,
                                            int(project_id)))

@app.route("/add")
@login_required
def add():
    global db
    return render_template("add.html", **locals())

@app.route("/login", methods=["GET", "POST"])
def login():
    authorized = False
    if request.method == "POST":
        # Check if user is in JSON DB.
        for user in users:
            username = request.form["username"]
            password = request.form["password"]
            if (username == user["username"]
                and password == user["password"]):
                # Handle the login
                username = User(username)
                login_user(username)
                authorized = True
                break

        if not authorized:
            flash("Invalid login, please try again.", "error")
        elif authorized:
            flash("Login succesful.", "success")
            return redirect(url_for("add"))

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "Logged ya out, brosef."

@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"), 404

@app.errorhandler(401)
def invalid_login(error):
    return render_template("access_denied.html"), 401
if __name__ == "__main__":
    app.run(debug=True)
