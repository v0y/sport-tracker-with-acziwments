getEvents = ->
    return [{
            title: 'Bieganie 10.54 km',
            start: new Date(),
            allDay: true,
            url: 'http://google.com/',
            color: '#f18d05'
        },{
            title: 'Bieganie 10.54 km',
            start: new Date(),
            allDay: true,
            url: 'http://google.com/',
        }]

drawCalendar = (events) ->
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
    })

$ ->
    events = getEvents()
    drawCalendar(events)
