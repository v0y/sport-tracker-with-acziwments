getWorkoutId = ->
    url = document.URL.split("//")[1].split("#")[0].split("/")
    url[3]


getJsonData = ->
    # get json data for chart

    $.ajax
        url: "/workouts/api"
        type: "POST"
        dataType: "json"
        data:
            workout_id: getWorkoutId()
            csrfmiddlewaretoken: $.cookie('csrftoken')
        error: (jqXHR, textStatus, errorThrown) -> console.log("AJAX Error: #{errorThrown}")
        success: (data) -> getChartData(data)


getChartData = (jsonData) ->
    # get data formatted for chart
    chartData = [
        {
            color: "#61AE24"
            key: "Tempo (min/km)"
            values: jsonData
        }
    ]

    nv.addGraph([])

nv.addGraph = (chartData) ->
    # chow chart
    chart = nv.models.lineChart()
        .useInteractiveGuideline(true)
        .margin({bottom: 70, left: 75})

    chart.xAxis
        .axisLabel('Dystans')
        .tickFormat (d3.format(",.1f"))

    chart.yAxis
        .axisLabel("Tempo")
        .tickFormat(d3.format(",.1f"))

    $chart = d3.select('.workout-chart svg')

    $chart
        .datum(chartData)
        .transition().duration(500).call(chart)

    nv.utils.windowResize -> $chart.call(chart)

    chart


$ ->
    moment.locale('pl')
    getChartData([])
