import json

def load(filename):
    """ Loads JSON formatted project data from a file and
    returns a list of all projects, sorted after number."""
    with open(filename, "r") as json_db:
        db = json.load(json_db)
        db = sorted(db, key=lambda project: project["project_id"])
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
    returned_projects = []

    # Filter by techniques
    if techniques != None:
        techniques = set(techniques)
        for project in db:
            if set(project["techniques_used"]) >= techniques:
                filtered_projects.append(project)
    else:
        filtered_projects = db

    # Filter by search
    searched_projects = []
    if search != None:
        for project in filtered_projects:
            append = False
            for field in search_fields:
                if field == "techniques_used":
                    field_content =  str(project.get(field))
                else:
                    field_content = project.get(field)
                if field_content.find(search) != -1:
                    append = True
            if project not in searched_projects and append == True:
                searched_projects.append(project)

    if techniques == None and search != None:
        return searched_projects
    else:
        return filtered_projects

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

db = load("tests/data.json")

project = get_project(db, 1)
#print(project)

techniques = get_techniques(db)
#print(techniques)

tech_stats = get_technique_stats(db)
print(tech_stats)

search_result = search(db, techniques=None,
                       search_fields=["course_id"], search="0")

for item in search_result:
  #  print(item["techniques_used"])
  #  print(item["course_id"])
    pass
  
