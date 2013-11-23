
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
        handleMapOnFileUploadSuccess(mapHandler, routes)
        # fill form fields
        fillFormFields(routeId, mapHandler)
    # alert if something went wrong
    else if xhr.readyState==4
        alert("Something went wrong. Error" + xhr.status)


handleMapOnFileUploadSuccess = (mapHandler, routes) ->
    # check if map was initialized
    if not mapHandler.map
        mapHandler.initializeMap()
    # draw routes on map
    mapHandler.singleNewRoute(routes)
    # show map canvas
    $("#map-canvas").show()


fillFormFields = (routeId, mapHandler) ->
    # route id
    $('#id_route_id').val(routeId)
    # distance
    $('#id_distance').val(mapHandler.distance)
    # start date
    $('#id_datetime_start').val(mapHandler.startTime.format('DD-MM-YYYY'))
    # start time
    $('#id_time_start').val(mapHandler.startTime.format('HH:mm'))
    # duration
    $('#id_duration_hours').val(mapHandler.duration.hours())
    $('#id_duration_mins').val(mapHandler.duration.minutes())
    $('#id_duration_secs').val(mapHandler.duration.seconds())


###############################################################################
# Run
###############################################################################

main = ->
    $("#map-canvas").hide()

    mapHandler = new RoutesMapHandler()

    # bind to form file input change event
    bindToFileInputChange(mapHandler)

$ ->
    main()
