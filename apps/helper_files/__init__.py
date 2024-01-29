def label_generator(data_to_plot):

    counter = 0
    seperator = 0

    total_label_generator = ""
    total_data_label_generator = ""

    for variable in data_to_plot:

        label_generator = """
                                            <label class="btn btn-sm btn-primary btn-simple %active_label" id="%id">
                                            <input type="radio" name="options" %checked_label>
                                            <span class="d-none d-sm-block d-md-block d-lg-block d-xl-block">%label</span>
                                            <span class="d-block d-sm-none">
                            <i class="tim-icons icon-single-02"></i>
                        </span>
                                        </label>    
        """

        data_label_generator = """$("#%id").click(function () {
            var data = myChartData.config.data;
            data.datasets[0].data = %data;
            data.labels = %label;
            myChartData.update();
        });"""

        if counter == 0:
            active_label = 'active'
            checked_label = 'checked class="d-none d-sm-none"'
        else:
            active_label = ''
            checked_label = 'class="d-none d-sm-none"'

        label_generator = label_generator.replace("%label", variable).replace("%id", str(counter))\
            .replace("%active_label", active_label).replace("%checked_label",checked_label)
        data_label_generator = data_label_generator.replace('%id', str(counter)).replace('%data', str(data_to_plot[variable][1]))\
            .replace('%label', str(data_to_plot[variable][0]))

        if counter == 0:
            total_label_generator += '<div class="row">'

        if seperator == 10:
            total_label_generator += '</div>'
            total_label_generator += '<div class="row">'
            seperator = 0

        total_label_generator += label_generator
        total_data_label_generator += data_label_generator

        counter +=1
        seperator +=1

    total_label_generator += '</div>'

    return total_label_generator, total_data_label_generator