# -*- encoding: utf-8 -*-
from apps.home import blueprint
from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from apps.helper_files.forms import CSVUploadForm
from apps.helper_files import label_generator
from markupsafe import Markup
import csv
import io

@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500

@blueprint.route('/monthly_data', methods=['GET'])
@login_required
def show_geotiff():
    # Read the GeoTIFF file
    geotiff_url = "https://test-implify-test.s3.eu-central-1.amazonaws.com/wc2.1_30s_tavg/con_1.png"

    return render_template('home/geo_tiff.html', img_url=geotiff_url)

@blueprint.route('/fetch-new-pic', methods=['GET'])
def update_geotiff():
    # Read the GeoTIFF file
    month = request.args.get('month')
    geotiff_url = "https://test-implify-test.s3.eu-central-1.amazonaws.com/wc2.1_30s_tavg/con_"+str(month)+".png"

    return jsonify({'image_url': geotiff_url})

@blueprint.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_csv():
    form = CSVUploadForm()
    if request.method == 'POST':
        if form.validate():
            csv_file = request.files['csv_file']

            if not csv_file:
                return render_template('home/page-no-data.html', error='No csv file selected.')

            reader = csv.DictReader(io.TextIOWrapper(csv_file, encoding='utf-8'))
            columns_to_select = form.column_names.data.split(',')

            # raise error
            if len(columns_to_select) != 3:
                return render_template('home/page-no-data.html', error='Need 3 variables to be selected (x-axis, y-axis and variable to select upon)')

            x_data_column_name = columns_to_select[0]
            y_data_column_name = columns_to_select[1]
            z_data_column_name = columns_to_select[2]
            sliced = form.slicer.data.split(',')
            sliced_comp = {}
            for slice_sub in sliced:
                try:
                    sliced_comp[slice_sub.split('=')[0]] = slice_sub.split('=')[1]
                except:
                    print("slicing failed")
            data_to_plot = {}

            # Check if user matches columns
            for row in reader:
                # build in check
                add_data = True
                for slice_key in sliced_comp:
                    if row[slice_key].lower().replace(" ", "") != sliced_comp[slice_key].lower().replace(" ", ""):
                        add_data = False
                if add_data:
                    if row[z_data_column_name] in data_to_plot:
                        sub_data = data_to_plot[row[z_data_column_name]]
                        sub_data[0].append(row[x_data_column_name])
                        sub_data[1].append(row[y_data_column_name])
                    else:
                        sub_data = [[row[x_data_column_name]], [row[y_data_column_name]]]

                    data_to_plot[row[z_data_column_name]] = sub_data

            # Process valid data
            label, label_gen = label_generator(data_to_plot)

            if len(data_to_plot) == 0:
                return render_template('home/page-no-data.html', error='No data based on your selection')

            return render_template('home/index.html',variables_selected=form.slicer.data,
                                   data_to_pass=data_to_plot[list(data_to_plot.keys())[0]]\
                                   , labels=Markup(label),label_gen= Markup(label_gen))
        else:
            return render_template('home/page-500.html')

    return render_template('home/upload.html', form=form)

@blueprint.route('/profile')
@login_required
def profile():
    return render_template('home/profile.html', username=current_user.username, email=current_user.email)

# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
