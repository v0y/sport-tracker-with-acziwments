getCurrentWorkoutId = ->
    # get current workout id
    parsedUrl = document.URL.split("//")[1].split("#")[0].split("/")
    parsedUrl[parsedUrl.length - 1]


main = ->
    $.ajax
        url: "/workouts/api/get/all"
        type: "POST"
        dataType: "json"
        data:
            current_workout_pk: getCurrentWorkoutId()
            csrfmiddlewaretoken: $.cookie('csrftoken')
        error: (jqXHR, textStatus, errorThrown) -> console.log("AJAX Error: #{errorThrown}")
        success: (data) ->
            drawCalendar(data)


drawCalendar = (events, current_month, current_year) ->
    $('.js-workouts-calendar').fullCalendar(
        header:
            left: 'prev,today,next'
            center: 'title'
            right: ''
        editable: false
        lang: 'pl'
        firstDay: 1  # monday
        aspectRatio: 3
        events: events
        eventColor: '#61ae24'
        timezone: 'local'
        timeFormat: 'HH:mm'
        defaultDate: moment().format('YYYY-MM-DD')
        height: 500
    )

$ ->
    main()
