
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_wtf.file import FileField,FileAllowed
from wtforms.validators import DataRequired, Length
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_ckeditor.fields import CKEditorField
from ..models import Courses

#This Function retrun All Courses From Course Tabel 
def select_coures():
    return Courses.query.all()

# New Lesson Form
class NewLessonForm(FlaskForm):

    course = QuerySelectField("Select Course", query_factory=select_coures, get_label="title", validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired(), Length(min=3, max=25)])
    content = CKEditorField("Content", validators=[DataRequired()], render_kw={"rows":"5"})
    slug = StringField("Slug", validators=[DataRequired(), Length(max=32)], render_kw={"placeholder":"Slug SEO"}) 
    image = FileField("Lesson Image", validators=[FileAllowed(["png", "jpg"])])
    submit = SubmitField("Add Lesson")


# Inherit From New Lesson Class
class UpdateLessonForm(NewLessonForm):
    
    image = FileField("Lesson Image", validators=[FileAllowed(["png", "jpg"])])
    update = SubmitField("Update")   