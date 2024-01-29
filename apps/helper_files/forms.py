
from flask_wtf import FlaskForm
from wtforms import StringField, FileField


# csv upload
class CSVUploadForm(FlaskForm):
    csv_file = FileField('Choose a CSV file')
    column_names = StringField('Enter column names to plot (1st will be x-axis, 2nd y-axis and 3rd to select variable)')
    slicer = StringField('Filter on following (column as key and variable as value, see example in placeholder):')