from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from flask_wtf.file import FileField,FileAllowed
from wtforms.validators import DataRequired, Length


# New Course Form
class CourseForm(FlaskForm):

    title = StringField("Title", validators=[DataRequired(), Length(max=50)])
    description = TextAreaField("Description", validators=[DataRequired()], render_kw={"rows":"4"})
    thumbnail = FileField("Thumbnail", validators=[DataRequired(), FileAllowed(["jpg", "png"])])
    submit = SubmitField("Create")
