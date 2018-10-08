from flask import Flask, render_template, url_for, request, redirect
from flask import abort
import data

# The base flask application
app = Flask(__name__)

# The JSON data loaded in a python
# friendly format
db = data.load("data.json")

def get_menu():
    """ Builds a list of routing strings for any
    route that is specified as /x and not /x/* 
    for use in the navigation menu.
    """
    menu_routes = []
    for rule in app.url_map.iter_rules():
        rule = str(rule).split("/")
        if len(rule) == 2 and rule[1] != "":
            menu_routes.append(rule[1])
        elif rule[1] == "":
            menu_routes.append("index")
    return menu_routes

@app.route("/bootstrap")
def bootstrap():
    return render_template("index_bootstrap.html")
@app.route("/hej/<asd>")
def hej(quest):
    pass

@app.route("/")
def index():
    """ Builds the index routing with menu items."""
    menu_routes = get_menu()
    database=db
    return render_template("index.html", **locals())

@app.route("/techniques")
def techniques():
    master_list= []
    technique_list = data.get_techniques(db)
    for e in technique_list:
        temp_list = [e]
        temp_list.append(data.search(db, techniques=[e]))
        master_list.append(temp_list)
    return render_template("techinques.html", master_list=master_list)

@app.route("/list", methods=["POST", "GET"])
def list():
    menu_routes = get_menu()
    technique_data = data.get_techniques(db)
    search_fields = data.get_searchfields(db)

    if request.method == "POST":
        search = request.form["search"]
        techniques = request.form.getlist("technique")
        searched_fields = request.form.getlist("field")
        requested_projects = data.search(db, search=search,
                                         search_fields=searched_fields,
                                         techniques=techniques)
        return render_template("list.html", **locals())
    else:
        search = ""
        techniques = []
        requested_projects = []
        return render_template("list.html", **locals())


@app.route("/project/<project_id>")
def project(project_id):
    menu_routes = get_menu()
    try:
        project = data.get_project(db, int(project_id))
    except:
        abort(404)
    if project:
        return render_template("project.html", **locals())
                           
@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"), 404

if __name__ == "__main__":
    app.run(debug=True)

