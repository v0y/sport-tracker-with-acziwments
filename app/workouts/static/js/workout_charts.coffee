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
        error: (jqXHR, textStatus, errorThrown) -> console.log("AJAX Error: #{errorThrown}")
        success: (data) -> generateChart(data)


generateChart = (jsonData) ->
    c3.generate(
        bindto: '.js-workout-chart'
        color:
            pattern: ['#e54028', '#00a1cb']
        data:
            xs:
                'pace-y': 'pace-x'
                'altitude-y': 'altitude-x'
            columns: jsonData
            axes:
                'pace-y': 'y'
                'altitude-y': 'y2'
            names:
                'pace-y': 'Pace',
                'altitude-y': 'Altitude'
            type: 'spline'
        axis:
            x:
                tick:
                    count: 20
                    format: d3.format('.2f')
            y:
                label:
                    text: 'kmph'
                    position: 'outer-middle'
                tick:
                    format: d3.format('.1f')
            y2:
                show: true
                label:
                    text: 'mamsl'
                    position: 'outer-middle'
                tick:
                    format: d3.format('.0f')
        grid:
            x:
                show: true
            y:
                show: true
        point:
            show: false
    )

$ ->
    moment.locale('pl')
    getJsonData()
