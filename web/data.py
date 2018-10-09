import json
import re

def load(filename):
    """ Loads JSON formatted project data from a file and
    returns a list of all projects, sorted after number."""
    try:
        with open(filename, "r") as json_db:
            db = json.load(json_db)
            db = sorted(db, key=lambda project: project["project_id"])
    except FileNotFoundError:
        return None
    except IsADirectoryError:
        return None
    return db

def load_users(filename):
    """ Loads JSON formatted user data from a file"""
    try:
        with open(filename, "r") as json_db:
            db = json.load(json_db)
    except FileNotFoundError:
        return None
    except IsADirectoryError:
        return None
    return db

def get_project_count(db):
    """ Retrieves the number of projects in a project list."""
    return len(db)

def get_project(db, i_d):
    """ Fetches the project with the specified id from the 
    specified list."""
    for project in db:
        key = project["project_id"]
        if key == i_d:
            return project

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
    """Fetches a list of all the techniques from the specified
    project list in lexicographical order."""
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
    """Collects and returns statistics for all techniques in 
    the specified project list."""
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
"""
db = load("data.json")

#search_result = search(db, techniques=None,
#search_fields=["course_id"], search="0")

search_result =  search(db, sort_by="end_date",  search='okänt', techniques=[],
                        search_fields=['project_id','project_name','course_name'])
#search_result = search(db)

for item in search_result:
    print(item)
    print("\n")

  
"""
