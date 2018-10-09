from flask import Flask, render_template, url_for, request, redirect
from flask import session, abort, flash, escape
import data
import os


app = Flask(__name__)
app.secret_key = os.urandom(64)
db = data.load("data.json")

# Database file of all the users and their passwords
users = data.load_users("users.json")

@app.route("/bootstrap")
def bootstrap():

    projects = data.search(db, search="")

    return render_template("index_bootstrap2.html", **locals())

@app.route("/")
def index():
    return render_template("index.html", database=db)

@app.route("/techniques")
def techniques():
    """Creates and sorts a list of all project by the technique used. Then it displays a page of all projects"""
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
    """Creates a page where you can search the database for projects and sort them"""
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
def add():
    if "logged_in" not in session:
        abort(401)
    global db
    return "Logged in as",  escape(session.get("logged_in"))
    return render_template("add.html", **locals())

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        for user in users:
            if (request.form["username"] == user["username"]
                and request.form["password"] == user["password"]):
                session["logged_in"] = request.form["username"]
                break
        
    return render_template("login.html", error=error)
    
@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"), 404

@app.errorhandler(401)
def invalid_login(error):
    return render_template("access_denied.html"), 401
if __name__ == "__main__":
    app.run(debug=True)

