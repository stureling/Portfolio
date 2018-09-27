import json

def load(filename):
    """ Loads JSON formatted project data from a file and
    returns a list of all projects, sorted after number."""
    with open(filename, "r") as json_db:
        db = json.load(json_db)
        db = sorted(db, key=lambda project: project[0]["project_id"])
        return db
        
def get_project_count(db):
    """ Retrieves the number of projects in a project list."""
    return len(db)

def get_project(db, i_d):
    """ Fetches the project with the specified id from the 
    specified list."""
    i_d = str(i_d)
    for project in db:
        key = project[0]["project_id"]
        if key == i_d:
            return project

def search(db, sort_by="start_date", sort_order="desc", techniques=None,
           search=None, search_fields=None):
    returned_projects = []

    # Filter by techniques
    if techniques != None:
        techniques = set(techniques)
        for project in db:
            if set(project[0]["techniques_used"]) >= techniques:
                returned_projects.append(project)
    else:
        returned_projects = db

    # Filter by search
    for project in returned_projects:
        for field in search_fields:
            if field in project[0]:
                if field.find(search):
                    print(field)
            
        
    return returned_projects

def get_techniques(db):
    """Fetches a list of all the techniques from the specified
    project list in lexicographical order."""
    techniques = []
    for project in db:
        project_techniques = project[0]["techniques_used"]
        for technique in project_techniques:
            if technique not in techniques:
                techniques.append(technique)
    techniques.sort()
    return techniques
        
def get_technique_stats(db):
    """Collects and returns statistics for all techniques in 
    the specified project list."""
    techniques = {}
    for project in db:
        project_techniques = project[0]["techniques_used"]
        for technique in project_techniques:
            if technique not in techniques:
                techniques[technique] = 1
            else:
                techniques[technique] += 1
    return techniques

db = load("testfile.json")

project = get_project(db, 1)
#print(project)

techniques = get_techniques(db)
#print(techniques)

tech_stats = get_technique_stats(db)
#print(tech_stats)

search_result = search(db, techniques=["html"],
                       search_fields=["course_name"], search="asdasd")
for item in search_result:
    print(item[0]["techniques_used"])
