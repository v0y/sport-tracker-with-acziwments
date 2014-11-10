###############################################################################
# Handle AJAX file upload
###############################################################################

bindToFileInputChange = (mapHandler) ->
    $form = $('#gpx-file-input-form')
    $form.find("input:file").change(->
        sendFile($form, mapHandler)
    )


sendFile = ($form, mapHandler) ->
    $inputField = $form.find("input:file")
    # validation
    if validateFileExtansion($inputField)
        # create an XHR request
        xhr = new XMLHttpRequest()
        # ...open the request...
        xhr.open("POST", $form.data('url'))
        # ...handle csrf...
        csrfToken = $.cookie('csrftoken')
        if csrfToken
            xhr.setRequestHeader("X-CSRFToken", csrfToken)
        # ...set up event listeners...
        xhr.onreadystatechange = ->
            fileUploadChangeState(xhr, mapHandler)
        # ... and send form.
        fd = new FormData($form.get(0))
        xhr.send(fd)


validateFileExtansion = ($inputField) ->
    extention = $inputField.val().split(".").pop().toLowerCase()
    if extention == 'gpx'
        return true;
    else
        alert("To nie jest właściwy rodzaj pliku - wybierz plik .gpx")
        return false;


fileUploadChangeState = (xhr, mapHandler) ->
    # if upload complete and successful
    if xhr.readyState==4 && xhr.status==200
        # get data from response
        response = JSON.parse(xhr.responseText)
        routeId = response['id']
        # response = {'id': 5, 'routesJSON': ...}
        routes = JSON.parse(response['tracks'])
        # display new route
        handleNewRoute(mapHandler, routes)
        # fill form fields
        fillFormFields(routeId, mapHandler)
        # show 'cancel button'
        $('#cancel-route').show()
    # alert if something went wrong
    else if xhr.readyState==4
        alert("Something went wrong. Error" + xhr.status)


handleNewRoute = (mapHandler, routes) ->
    mapHandler.initializeMap()
    # draw routes on map
    mapHandler.singleNewRoute(routes)
    # show map canvas
    $("#map-canvas").show()


fillFormFields = (routeId, mapHandler) ->
    # route id
    $('#id_route_id').val(routeId)
    # distance
    if $('#id_distance').val() == ''
        $('#id_distance').val(mapHandler.distance.toFixed(2))
    # manual routes will not have times
    if not mapHandler.startTime
        return

    # fill times only if duration is not filled already
    if $('#id_duration_hours').val() == '0' and
            $('#id_duration_mins').val() == '0' and
            $('#id_duration_secs').val() == '0'
        # adjust start time according to timezone
        startTime = moment.tz(mapHandler.startTime._d, "Europe/Warsaw")
        startTime.add('minutes', -startTime.zone())
        # start date
        $('#id_datetime_start').val(startTime.format('DD-MM-YYYY'))
        # start time
        $('#id_time_start').val(startTime.format('HH:mm:ss'))
        # duration
        $('#id_duration_hours').val(mapHandler.duration.hours())
        $('#id_duration_mins').val(mapHandler.duration.minutes())
        $('#id_duration_secs').val(mapHandler.duration.seconds())


###############################################################################
# Handle route download
###############################################################################

displayRelatedRoute = (routeId, url, mapHandler) ->
    $.ajax(
        url: url,
        data: {'route_id': routeId},
        success: (data, textStatus, jqXHR) ->
            handleNewRoute(mapHandler, JSON.parse(data['route']))
        ,
        dataType: 'json'
    )

###############################################################################
# Handle manual drawing of routes
###############################################################################

bindManualRouteSwitch = (mapHandler) ->
    $switch = $('#route-drawing-switch')
    $switch.on('click', ->
        # initialize map (if it's not initialized yet).
        mapHandler.initializeMap()

        if mapHandler.mode == 'readOnly'
            mapHandler.initializeManualRouteHandling()
            $('#cancel-route').show()
    )

bindSaveManualRoute = (mapHandler) ->
    $saveRouteButton = $('#manual-route-save')

    $saveRouteButton.on('click', ->
        routeData = mapHandler.getRouteDataFromMap()

        data = {
            'tracks': JSON.stringify(routeData),
            'csrfmiddlewaretoken': $.cookie('csrftoken')
        }

        $.ajax({
            url: $saveRouteButton.data('url'),
            data: data
            dataType: "json",
            type: "POST",
            timeout: 5000,
            success: (data, textStatus, jqXHR) ->
                routeId = data['id']
                routes = JSON.parse(data['tracks'])
                # display new route
                handleNewRoute(mapHandler, routes)
                # fill form fields
                fillFormFields(routeId, mapHandler)
            ,
            error: (jqXHR, textStatus, errorThrown) ->
                alert("Ups...\nNie udało się zapisać trasy.\n#{textStatus} - #{errorThrown}")
        })
    )


setMapHandlerControls = (mapHandler) ->
    controls = {
        container: $('#map-controls'),
        distanceDisplay: $('#map-total-distance'),
        useDirectionsControl: $('#use-google-directions'),
        travelModeControl: $('#travel-mode-select'),
        googleWarningsDisplay: $('#google-warnings')
    }

    mapHandler.controls = controls


###############################################################################
# Interface related functions
###############################################################################

bindControls = (mapHandler) ->
    # cancel button
    $cancel = $('#cancel-route')
    $cancel.on('click', ->
        # clear route id
        $('#id_route_id').val('')
        # hide map
        $("#map-canvas").hide()
        # remove all routes
        mapHandler.clearRoutes()
    )


###############################################################################
# Run
###############################################################################

main = ->
    # if there's no canvas then fail fast
    mapCanvas = $('#map-canvas')
    if mapCanvas[0]
        mapHandler = new RoutesMapHandler()
        # bind to form file input change event
        bindToFileInputChange(mapHandler)

        # bind drawing on map initialization...
        bindManualRouteSwitch(mapHandler)
        # ...and route save.
        bindSaveManualRoute(mapHandler)

        # if map canvas has a route-id data, then get that route with AJAX
        routeId = mapCanvas.data('route-id')
        if routeId
            displayRelatedRoute(routeId, mapCanvas.data('url'), mapHandler)
        else
            mapCanvas.hide()

        setMapHandlerControls(mapHandler)

        bindControls(mapHandler)

$ ->
    main()
