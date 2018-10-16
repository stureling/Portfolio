from wtforms import Form, BooleanField, StringField
from wtforms import validators, IntegerField, DateField
from wtforms import TextAreaField, ValidationError
import re

class_kw = "form-control text-light bg-dark"

class Database():
    def __init__(self, *args, **kwargs):
        pass
        
    

class ModifyForm(Form):
    """Form for modifying a project.
    
    

    """
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)
        
    start_date = StringField("Start Date")
    end_date = StringField("End Date")
    course_name = StringField("Course Name")
    long_description = TextAreaField("Long Description")
    short_description = TextAreaField("Short Description")
    group_size = IntegerField("Group Size")
    academic_credits = StringField("Academic Credits")
    external_link = StringField("External Link",
                                [validators.URL(), validators.Optional()])
    techniques_used = StringField("Techniques Used",
                                  [validators.Regexp("\w{1,}[,\n]{1,}",
                                                     flags=re.IGNORECASE, message="Please enter as comma-separated words.")])
    project_name = StringField("Project Name",
                               [validators.Length(min=1)])
    course_id = StringField("Course ID")
    project_id = IntegerField("Project ID",
                              [validators.InputRequired()])
    big_image = StringField("Big images")

class ModifyFormAdd(ModifyForm):

    def __init__(self, *args, **kwargs):
        self.db = kwargs["database"]
        super().__init__(*args, **kwargs)

    project_id = IntegerField("Project ID", [validators.InputRequired()])
    def validate_project_id(self, field):
        if field.data in  [x["project_id"] for x in self.db]:
            raise ValidationError("Project ID already in database.")
