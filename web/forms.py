from wtforms import Form, BooleanField, StringField
from wtforms import validators, IntegerField, DateField
from wtforms import TextAreaField, ValidationError

class_kw = "form-control text-light bg-dark"



class ModifyForm(Form):

    def __init__(self, *args,  **kwargs):
        self.db = kwargs["database"]
        super().__init__(*args, **kwargs)

    @property
    def _db(self):
        return self.db

    start_date = StringField("Start Date")
    end_date = StringField("End Date")
    course_name = StringField("Course Name")
    long_description = TextAreaField("Long Description")
    short_description = TextAreaField("Short Description")
    group_size = IntegerField("Group Size")
    academic_credits = StringField("Academic Credits")
    external_link = StringField("External Link", [validators.URL(), validators.Optional()])
    techniques_used = StringField("Techniques Used")
    project_name = StringField("Project Name",
                               [validators.Length(min=1)])
    course_id = StringField("Course ID")
    project_id = IntegerField("Project ID", [validators.InputRequired()])
    def validate_project_id(self, field):
        if field.data in  [x["project_id"] for x in self._db]:
            raise ValidationError("Project ID already in database.")
    big_image = StringField("Big images")

