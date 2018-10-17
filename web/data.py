import json
import re

def load(filename):
    try:
        with open(filename, "r") as json_db:
            db = json.load(json_db)
            db = sorted(db, key=lambda project: project["project_id"])
    except FileNotFoundError:
        return None
    except IsADirectoryError:
        return None
    return db

def save(database, filename):
    """ Saves the database to file
    
    Function takes in a database in the form of a list and saves it to the
    desired filename in the current working directory.

    Parameters
    ----------
    database : list
       The database to be modified, as a list.
    filename : str
       The file to save to, as as string.

    """
    try:
        new_json = json.dumps(database, indent=4)
        with open(filename, "w") as f:
            for line in new_json:
                f.write(line)
    except:
        return None

def load_users(filename):
    """ Loads users from file

    Loads JSON formatted user data from a specified file.
    
    Parameters
    ----------
    filename : str
       The file to read from.

    """
    try:
        with open(filename, "r") as json_db:
            db = json.load(json_db)
    except FileNotFoundError:
        return None
    except IsADirectoryError:
        return None
    return db

def get_project_count(db):
    return len(db)

def get_project(db, i_d):
    for project in db:
        key = project["project_id"]
        if key == i_d:
            return project

def remove_project(db, i_d):
    """ Removes a project

    Function removes a project with a certain ID from the
    database list.

    Parameters
    ----------
    db : list
       The list to remove the project from.
    i_d : int
       The project_id to remove, as an int.

    """
    project = get_project(db, i_d)
    if project in db:
        db.remove(project)
            
        
def search(db, sort_by="start_date", sort_order="desc", techniques=None,
           search=None, search_fields=None):
    
    technique_projects = []
    search_projects = []
    output = []
    reverse_order = False

    if sort_order == "desc":
        reverse_order = True

    if not search_fields and search_fields != []:
        search_fields = get_searchfields(db)

    # Filter by technique    
    if techniques and len(techniques) > 0:
        techniques = set(techniques)
        for project in db:
            if set(project["techniques_used"]) >= techniques:
                technique_projects.append(project)
                
    # Filter by search
    if search:
        for project in db:
            append = False
            for field in search_fields:
                field_content =  str(project.get(field))
                if re.search(search, field_content, re.IGNORECASE):
                    append = True
            if append == True:
                search_projects.append(project)

    # Collate results
    if search and not techniques:
        output = search_projects
    elif techniques and not search:
        output = technique_projects
    elif search and techniques:
        for project in db:
            if project in technique_projects and project in search_projects:
                output.append(project)
    elif not search and not techniques:
        output = db
                        
    return sorted(output, key=lambda project: project[sort_by],
                  reverse=reverse_order)
        
def get_techniques(db):
    techniques = []
    for project in db:
        project_techniques = project["techniques_used"]
        for technique in project_techniques:
            if technique not in techniques:
                techniques.append(technique)
    techniques.sort()
    return techniques

def get_searchfields(db):
    search_fields = []
    for project in db:
        for key in project:
            if key not in search_fields:
                search_fields.append(key)
    return search_fields

def get_technique_stats(db):
    techniques = {}
    
    # Build up a list of all the techniques used.
    for project in db:
        for technique in project["techniques_used"]:
            if technique not in techniques:
                techniques[technique] = []

    # Append to the list of projects.
    for project in db:
        for technique in project["techniques_used"]:
            techniques[technique].append({"id":project["project_id"],
                                          "name":project["project_name"]})
            
    return techniques
