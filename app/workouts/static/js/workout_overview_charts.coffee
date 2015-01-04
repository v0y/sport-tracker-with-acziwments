String::endsWith ?= (s) -> s == '' or @slice(-s.length) == s


parseUrl = ->
    url = document.URL.split("//")[1].split("#")[0].split("/")
    {
        user: url[4]
        dataType: url[5]
        rangeType: url[6]
        date: url[7]
    }

dateFormat = ->
    rangeType = parseUrl().rangeType

    switch rangeType
        when 'all-time' then xFormat = '%Y-'
        when 'year' then xFormat = '%Y-%m'
        when 'month' then xFormat = '%Y-%m-%d'

    switch rangeType
        when 'all-time' then labelFormat = '%Y'
        when 'year' then labelFormat = '%Y-%m'
        when 'month' then labelFormat = '%Y-%m-%d'

    {xFormat: xFormat, labelFormat: labelFormat}


getJsonData = ->
    # get json data for chart

    urlData = parseUrl()

    $.ajax
        url: $('.js-workouts-overview-chart').data('url')
        type: "POST"
        dataType: "json"
        data:
            user: urlData.user
            data_type: urlData.dataType
            range_type: urlData.rangeType
            date: urlData.date
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
            xFormat: dateFormat().xFormat
            groups: [xLabels]
        axis:
            x:
                type: 'timeseries'
                tick:
                    format: dateFormat().labelFormat
                    culling: false
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
