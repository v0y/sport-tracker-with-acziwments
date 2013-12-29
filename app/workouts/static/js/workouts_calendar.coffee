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
            drawCalendar(
                data['events'],
                data['current_month'],
                data['current_year']
            )


drawCalendar = (events, current_month, current_year) ->
    $('#calendar').fullCalendar({
        header: {
            left: 'prev,today,next',
            center: 'title',
            right: '',
        },
        editable: false,
        dayNames: ['Niedziela', 'Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota'],
        dayNamesShort: ['Nie', 'Pon', 'Wt', 'Śr', 'Czw', 'Pią', 'Sob'],
        weekNumberTitle: 'Tydz.',
        monthNames: ['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec',
                     'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień'],
        monthNamesShort: ['Sty', 'Lut', 'Mar', 'Kwie', 'Maj', 'Cze', 'Lip', 'Sier', 'Wrz', 'Paź', 'Lis', 'Gru'],
        buttonText: {
            today: 'dzisiaj',
            month: 'miesiąc'
        },
        firstDay: 1,  # monday
        aspectRatio: 3,
        events: events,
        eventColor: '#61ae24',
        month: current_month,
        year: current_year,
    })

$ ->
    main()
