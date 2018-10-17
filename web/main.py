from flask import Flask, render_template, url_for, request, redirect
from flask import session, abort, flash, escape
import data
import os
from flask_login import LoginManager, login_user, login_required, UserMixin
from flask_login import logout_user
import forms

# Start Flask
app = Flask(__name__)
app.secret_key = "\xe1TL\\xc4?~\\xc4\\x91\\xa49E|m3qrQ\\xb7\'F\\x18<\\xa5\\xe1kJ\\xb8\\x89\\xa9\\xa8>\\xc7&\\x16\\xb6\\xe0\\x86\\xa7m\\xc4]Mg\\xdf\\xe0\\x8c\\xa3Ts\\xaa]\\xc1\\xf1Q,\\x9c\\xa5\\xe7-\\xd9\\xda\\xb2\\xf1\\xf3"
db = data.load("data.json")


class User(UserMixin):
    """Flask login user

    This is a basic user template for flask_login that inherits
    from flask_login's UserMixin class.

    Attributes
    ----------
    id : int
       An integer representing the user's id.

    """
    def __init__(self, user_id):
        """ __init method___

        Starts the user off with an id.

        Parameters
        ----------
        user_id : int
           An integer representing the user's id.

        """
        self.id = user_id

# Database file of all the users and their passwords
users = data.load_users("users.json")

# Start Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    """ Callback for login_user

    This is a callback function for flask login.
    It's called every time we try to log in a user with
    flask_login.login_user.

    Parameters
    ----------
    user_id: int
       User representation.
    """
    return User(user_id)


# Start Flask routes
@app.route("/")
def index():
    """ Index view

    Returns a view for the index page. Fetches
    all the projects in the database and passes them
    on to render_template function together with the index.html
    template page.

    Returns
    -------
    render_template

    """
    latest_projects = data.search(db, sort_by='end_date')
    return render_template("index.html", database=db,
                           latest_projects=latest_projects)

@app.route("/techniques")
def techniques():
    """ Technique view

    Returns a view of the technique page with each technique on its own
    row, together with its relevant projects.

    Returns
    -------
    render_template

    """

    db = data.load("data.json")
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
    """List view

    Returns a view of the list page. Utilises the HTML POST
    method to request data from user for use in database search.

    If the method is POST the function will request projects from the
    data.search function and pass them on to the render_template
    method. If the method is GET it will simply return all projects
    from data.search to render_template.

    Returns
    --------
    render_template

    """
    db = data.load("data.json")
    technique_data = data.get_techniques(db)
    search_fields = data.get_searchfields(db)

    if request.method == "POST":
        search = request.form["search"]
        techniques = request.form.getlist("techniques")
        searched_fields = request.form.getlist("searched_fields")
        if request.form["sort"]:
            sort = request.form["sort"]
        else:
            sort = "start_date"
        order = request.form["order"]
        requested_projects = data.search(db,
                                         search=search,
                                         search_fields=searched_fields,
                                         techniques=techniques,
                                         sort_by=sort,
                                         sort_order=order)
        return render_template("list.html",**locals())
    else:
        requested_projects = data.search(db)
        return render_template("list.html", **locals())

@app.route("/project/<project_id>")
def project(project_id):
    """Project view

    Returns a view of the project page. Takes as input a GET
    variable from Flask's route method and requests the desired
    project from the database based upon this integer value.

    Parameters
    ----------
    project_id : int
       The integer representing the desired project_id key in
       the database.

    Returns
    --------
    render_template

    """
    db = data.load("data.json")
    if project_id.isdigit():
        valid_project = data.get_project(db, int(project_id))
        if valid_project:
            return render_template("project.html",
                                   project=data.get_project(db,
                                                            int(project_id)))
        else:
            abort(404)
    else:
        abort(404)

@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    """Edit view

    Returns a view of the edit page. The edit page is a list of
    all the currently existing projects in the database.

    Returns
    -------
    render_template

    """
    db = data.load("data.json")
    global db
    # Delete project
    if request.method == "POST":
        data.remove_project(db, int(request.form["delete"]))
        data.save(db, "data.json")
        flash("Project deleted.", "success")
        
    all_projects = data.search(db, search="")
    table_fields = ["project_id",
                    "project_name",
                      "short_description",
                    "course_id"]
    return render_template("add.html", **locals())

@app.route("/modify/<project_id>", methods=["GET", "POST"])
@login_required
def modify(project_id):
    """Modify view

    Returns a view of the modify page. The modify page supports both
    HTML GET and POST methods. The GET method is used to request
    the desired project, and is passed into the modify function through
    Flask's routing method. This data is then used to populate the
    fields on the page. The POST method is used to populate the WTForm
    instance, which is then used to edit the actual database.


    Parameters
    ----------
    project_id : int
        The integer representing the desired project_id key in
    the database.

    Returns
    ----------
    render_template

    """
    db = data.load("data.json")
    if project_id == "add":
        form = forms.ModifyFormAdd(request.form, database=db)
        # Add new project.
        if request.method == "POST" and form.validate():
            flash("Project modified successfully.", "success")
            db.append({})
            for k,v in form.data.items():
                if k == "techniques_used":
                    v = v.split(" ")
                db[-1][k] = v

            data.save(db, "data.json")
    elif  (project_id.isdigit() and
           int(project_id) in  [x["project_id"] for x in db]):
        # Get current project and its index
        project = data.search(db, search=project_id,
                              search_fields=["project_id"])
        p_index = db.index(project[0])
        form = forms.ModifyForm(request.form,
                               data=project[0], database=db)
        # Modify the project.
        if request.method == "POST" and form.validate():
            flash("Project modified successfully.", "success")
            for k,v in form.data.items():
                if project[0][k] != v:
                    if k == "techniques_used":
                        print(v.split(" "))
                        v = v.split(" ")
                project[0][k] = v

            data.save( db, "data.json")

    else:
        abort(404)

    # Instantiated WTForm of ModifyForm type
    class_kw = forms.class_kw

    return render_template("modify.html", **locals())

@app.route("/login", methods=["GET", "POST"])
def login():
    """Login view

    Returns a view of the login page. The login page lets you log in
    if you aren't yet authenticated. If the login is successful, it
    redirects to the edit view. HTML GET and POST methods are used
    to get the data from the end user.

    Returns
    -------
    render_template


    """
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
            flash("Invalid login, please try again.", "danger")
        elif authorized:
            return redirect(url_for("edit"))

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    """Logout view

    Returns logout view as well as logs the user out with flask_login.
    logout_user().

    Returns
    --------
    string

    """
    logout_user()
    return redirect(url_for("index"))

@app.errorhandler(404)
def page_not_found(error):
    """404 view

    Returns 404 view for page not found.

    Returns
    -------
    render_template


    """
    return render_template("page_not_found.html"), 404

@app.errorhandler(401)
def invalid_login(error):
    """401 view

    Returns the 401 view for not authenticated.

    Returns
    --------
    render_template


    """
    flash('You are not logged in.', "warning")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
