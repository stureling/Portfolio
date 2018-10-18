from wtforms import Form, BooleanField, StringField
from wtforms import validators, IntegerField, DateField
from wtforms import TextAreaField, ValidationError, MultipleFileField
import re

class_kw = "form-control text-dark bg-light"

class ModifyForm(Form):
    """Form for modifying a project.
    
    It has several fields of various types (StringField, 
    IntegerField, FileField, etc.) that correspond to the
    indexes in the project's dictionary, which are specified in the
    project specification. Please refer to:
    `LiU Documentation <https://www.ida.liu.se/~TDP003/current/projekt/dokument/systemspecifikation.pdf>`_

    
    Parameters
    -----------
    *args : *args
       Any number of positional arguments.
    **kwargs : **kwargs
       Any number of keyword arguments.
    """
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)
        
    pattern = "^([\d]{4})-([0][0-9]|[1][0-2])-([0][1-9]|[1-2][1-9]|[3][0-1])$"
        
    start_date = StringField("Start Date",
                             validators=[validators.Regexp(pattern,
                                                           message="Please enter date in format YYYY-MM-DD."),
                                         validators.Optional()])
    end_date = StringField("End Date",
                           validators=[validators.Regexp(pattern,
                                                         message="Please enter date in format YYYY-MM-DD."),
                                       validators.Optional()])
    course_name = StringField("Course Name")
    long_description = TextAreaField("Long Description")
    short_description = TextAreaField("Short Description")
    group_size = IntegerField("Group Size", [validators.Optional()])
    academic_credits = StringField("Academic Credits")
    external_link = StringField("External Link",
                                [validators.URL(), validators.Optional()])
    techniques_used = StringField("Techniques Used",
                                  filters=[lambda x: re.sub("(\[)|'|\]|,", "", str(x))],
                                  validators=[validators.Regexp("[a-z]",
                                                     flags=re.IGNORECASE, message="Please enter at least one technique.")])
    project_name = StringField("Project Name",
                               [validators.Length(min=1)])
    course_id = StringField("Course ID")
    project_id = IntegerField("Project ID",
                              [validators.InputRequired()])
    images = MultipleFileField("Image File")

class ModifyFormAdd(ModifyForm):
    """ Form for adding new projects
    
    Like ModifyForm, except it inherts a validations method for 
    the project_id field in order to avoid conflicts with other
    projects already in the database.

    Parameters
    -----------
    *args : *args
       Any number of positional arguments.
    **kwargs : **kwargs
       Any number of keyword arguments.


    """
    def __init__(self, *args, **kwargs):
        self.db = kwargs["database"]
        super().__init__(*args, **kwargs)

    project_id = IntegerField("Project ID", [validators.InputRequired()])
    def validate_project_id(self, field):
        if field.data in  [x["project_id"] for x in self.db]:
            raise ValidationError("Project ID already in database.")
