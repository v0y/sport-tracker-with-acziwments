String::endsWith ?= (s) -> s == '' or @slice(-s.length) == s


getJsonData = ->
    # get json data for chart
    $.ajax
        url: $('.js-workouts-overview-chart').data('url')
        type: "POST"
        dataType: "json"
        data:
            csrfmiddlewaretoken: $.cookie('csrftoken')
        error: (jqXHR, textStatus, errorThrown) -> console.log("AJAX Error: #{errorThrown}")
        success: (data) -> generateChart(data)


generateChart = (jsonData) ->
    xs = {}
    xLabels = []
    for column in jsonData
        label = column[0]
        if label.endsWith('-x')
            xLabel = label.split('-')[0]
            xs[xLabel] = label
            xLabels.push(xLabel)

    c3.generate(
        bindto: '.js-workouts-overview-chart'
        color:
            pattern: ['#113f8c', '#d0d102', '#01a4a4', '#e54028', '#00a1cb',
                      '#f18d05', '#61ae24', '#d70060', '#32742c', '#616161']
        data:
            xs: xs
            columns: jsonData
            type: 'bar'
            xFormat: '%Y-'
            groups: [xLabels]
        axis:
            x:
                type: 'timeseries'
                tick:
                    format: '%Y'
            y:
                label:
                    text: 'km'
                    position: 'outer-middle'
                tick:
                    format: d3.format('.1f')
        grid:
            x:
                show: true
            y:
                show: true
    )

$ ->
    getJsonData()
