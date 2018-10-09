from flask import Flask, render_template, url_for, request, redirect
import data

app = Flask(__name__)

db = data.load("data.json")

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
    if request.method == "POST":
        search = request.form["search"]
        techniques = request.form.getlist("technique")
        search_fields = request.form.getlist("field")
        requested_projects = data.search(db, search=search,
                                         search_fields=search_fields,
                                         techniques=techniques)
        return render_template("list.html",
                               technique_data=data.get_techniques(db),
                               search_fields=data.get_searchfields(db),
                               techniques = techniques,
                               search = search,
                               requested_projects = requested_projects)
    else:
        return render_template("list.html",
                               technique_data=data.get_techniques(db),
                               search_fields=data.get_searchfields(db),
                               techniques = [],
                               search = "",
                               requested_projects = [])

@app.route("/project/<project_id>")
def project(project_id):
    if data.get_project(db, int(project_id)):
        return render_template("project.html",
                           project=data.get_project(db,
                                            int(project_id)))
@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"), 404

if __name__ == "__main__":
    app.run(debug=True)

