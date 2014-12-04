getWorkoutId = ->
    url = document.URL.split("//")[1].split("#")[0].split("/")
    url[3]


getJsonData = ->
    # get json data for chart

    $.ajax
        url: "/workouts/api/get/chart"
        type: "POST"
        dataType: "json"
        data:
            workout_id: getWorkoutId()
            csrfmiddlewaretoken: $.cookie('csrftoken')
            unit: $('.workout-chart svg').data('unit')
        error: (jqXHR, textStatus, errorThrown) -> console.log("AJAX Error: #{errorThrown}")
        success: (data) -> getChartData(data)


getChartData = (jsonData) ->
    # get data formatted for chart
    unit = $('.workout-chart svg').data('unit')
    chartData = [
        {
            color: "#61AE24"
            key: "Tempo (#{if unit == '1' then 'km' else 'mi'}/h)"
            values: jsonData.pace
            yAxis: 1
            type: 'line'
        },
        {
            color: "#00A1CB"
            key: "Wysokość (m npm)"
            values: jsonData.altitude
            yAxis: 2
            type: 'line'
        }
    ]
    nv.addGraph(chartData)

nv.addGraph = (chartData) ->
    unit = $('.workout-chart svg').data('unit')
    # chow chart
    chart = nv.models.multiChart()
        .margin({top: 30, right: 75, bottom: 70, left: 75})

    chart.xAxis
        .axisLabel("Dystans (#{if unit == '1' then 'km' else 'mi'})")
        .tickFormat(d3.format(",.1f"))

    chart.yAxis1
        .axisLabel("Tempo (#{if unit == '1' then 'km' else 'mi'}/h)")
        .tickFormat(d3.format(",.1f"))

    chart.yAxis2
        .axisLabel("Wysokość (m npm)")
        .tickFormat(d3.format(",.1f"))

    $chart = d3.select('.workout-chart svg')

    $chart
        .datum(chartData)
        .transition().duration(500)
        .call chart

    nv.utils.windowResize -> $chart.call chart

    chart


$ ->
    moment.locale('pl')
    getJsonData()
