from wtforms import Form, BooleanField, StringField
from wtforms import validators, IntegerField, DateField

class ModifyForm(Form):
    start_date = StringField("Start Date")
    end_date = StringField("End Date")
    course_name = StringField("Course Name")
    long_description = StringField("Long Description")
    group_size = IntegerField("Group Size")
    academic_credits = StringField("Academic Credits")
    external_link = StringField("External Link")
    techniques_used = StringField("Techniques Used")
    project_name = StringField("Project Name",
                               [validators.Length(min=1)])
    course_id = StringField("Course ID")
    project_id = IntegerField("Project ID")
    big_image = StringField("Big images")
