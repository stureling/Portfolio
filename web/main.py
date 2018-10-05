from flask import Flask, render_template, url_for, request, redirect
import data

app = Flask(__name__)

db = data.load("data.json")

@app.route("/")
def index():
    return render_template("index.html", database=db)

@app.route("/techniques", methods=["GET", "POST"])
def techniques():
    techniques = request.form.getlist("technique")
    return render_template("techniques.html",
                           technique_data=data.get_techniques(db),
                           techniques=techniques,
                           displayed_projects=data.search(db,
                                                          techniques=
                                                          techniques))

@app.route("/list", methods=["POST", "GET"])
def list():

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

