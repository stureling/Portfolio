from wtforms import Form, BooleanField, StringField
from wtforms import validators, IntegerField, DateField
from wtforms import TextAreaField, ValidationError
import re

class_kw = "form-control text-dark bg-light"

class ModifyForm(Form):
    """Form for modifying a project.
    
    It has several fields of various types that are interpreted
    by WTForms.

    """
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)
        
    start_date = StringField("Start Date")
    end_date = StringField("End Date")
    course_name = StringField("Course Name")
    long_description = TextAreaField("Long Description")
    short_description = TextAreaField("Short Description")
    group_size = IntegerField("Group Size", [validators.Optional()])
    academic_credits = StringField("Academic Credits")
    external_link = StringField("External Link",
                                [validators.URL(), validators.Optional()])
    techniques_used = StringField("Techniques Used",
                                  [validators.Regexp("[a-z]",
                                                     flags=re.IGNORECASE, message="Please enter at least one technique.")])
    project_name = StringField("Project Name",
                               [validators.Length(min=1)])
    course_id = StringField("Course ID")
    project_id = IntegerField("Project ID",
                              [validators.InputRequired()])
    big_image = StringField("Big images")

class ModifyFormAdd(ModifyForm):
    """ Form for adding new projects
    
    Like ModifyForm, except it inherts a validations method for 
    the project_id field in order to avoid conflicts with other
    projects already in the database.


    """
    def __init__(self, *args, **kwargs):
        self.db = kwargs["database"]
        super().__init__(*args, **kwargs)

    project_id = IntegerField("Project ID", [validators.InputRequired()])
    def validate_project_id(self, field):
        if field.data in  [x["project_id"] for x in self.db]:
            raise ValidationError("Project ID already in database.")
