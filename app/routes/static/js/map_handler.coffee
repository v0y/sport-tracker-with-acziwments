###############################################################################
# Map Handling
###############################################################################

class MapHandler
    mode: 'readOnly'
    map: null;
    routes: []

    activeRoute: null;

    directionsService: null;

    controls: null;

    initializeMap: ->
        styles = [{featureType: "poi", stylers: [{ visibility: "off" }]}]

        mapOptions = {
            center: new google.maps.LatLng(15, 15),
            zoom: 3,
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            styles: styles
        }
        @map = new google.maps.Map($("#map-canvas")[0], mapOptions)

    addRoute: (isManual) ->
        route = new Route()
        route.map = @map
        route.controls = @controls
        if isManual
            route.isManual = true;
        @routes.push(route)
        @activeRoute = route

        return route

    addRouteFromJson: (routeJson) ->
        route = @addRoute()
        route.tracks = routeJson
        route.draw()

        @getDistance()
        @getTimes()

    addManualRoute: ->
        route = @addRoute()

    clearRoutes: ->
        for route in @routes
            route.clear()

        @routes = []

    singleNewRoute: (routeJson) ->
        @clearRoutes()
        @finishManualRouteHandling()
        @addRouteFromJson(routeJson)

    getDistance: ->
        @distance = 0

        for route in @routes
            @distance += route.distance

        return @distance

    getTimes: ->
        @startTime = @routes[0].startTime
        @endTime = @routes[0].startTime

        for route in @routes
            if route.startTime < @startTime
                @startTime = route.startTime

            if route.endTime > @endTime
                @endTime = route.endTime

        if @endTime
            durationSeconds = @endTime.diff(@startTime, 'seconds')
            @duration = moment.duration(durationSeconds, 'seconds')

        return @duration

    toggleManualRouteDrawing: ->
        switch @mode
            when 'readOnly' then @initializeManualRouteHandling()
            when 'edit' then @finishManualRouteHandling()

    initializeManualRouteHandling: ->
        # clear existing routes (revert if possible)
        @clearRoutes()

        # get directions service object
        if not @directionsService
            @directionsService = new google.maps.DirectionsService();

        # show controls
        @controls.container.show()

        # create new route
        route = @addRoute(true)
        route.directionsService = @directionsService

        # initialize route to map bindings
        route.initializeMapBindings()

        # update handler mode
        @mode = 'edit'

    finishManualRouteHandling: ->
        if @activeRoute
            # unbind route to map events
            @activeRoute.removeMapBindings()

            # make markers undragable
            @activeRoute.makeMarkersUnDragable()

        # hide controls
        @controls.container.hide()

        # update handler mode
        @mode = 'readOnly'

    getRouteDataFromMap: ->
        if @mode == 'edit' and @activeRoute
            @finishManualRouteHandling()

            return @activeRoute.markersToTracks()
        else
            return null;

###############################################################################
# Route Class
###############################################################################

class Route
    map: null;
    tracks: null;

    isManual: false;

    polylines: []

    mapPoints: []
    distance: 0
    fullKmSectionsList: []

    startMarker: null;
    finishMarker: null;
    fullKmMarkers: []

    @latlngbounds: null;

    controls: null;

    draw: ->
        @drawTracks()
        @addStartFinishMarkers()
        fullKmSectionsList = @getRouteDistance()
        @drawFullKmMarkers(fullKmSectionsList)
        @getStartFinishTimes()
        # center / zoom map
        @map.fitBounds(@latlngbounds)

    clear: ->
        for marker in @fullKmMarkers
            marker.setMap(null)

        @fullKmMarkers = []

        if @startMarker
            @startMarker.setMap(null)
        if @finishMarker
            @finishMarker.setMap(null)

        for polyline in @polylines
            polyline.setMap(null)

        @polylines = []

    drawTracks: ->
        @clear()

        # object for handling initial map zoom level and center
        @latlngbounds = new google.maps.LatLngBounds()

        # add points to map
        for track in @tracks
            trackMapPoints = []
            for segment in track['segments']
                # get google map points array
                segmentMapPoints = []
                for point in segment
                    pt = new google.maps.LatLng(point['lat'], point['lon'])
                    segmentMapPoints.push(pt)
                    @latlngbounds.extend(pt)

                # create new polyline
                polyline = new google.maps.Polyline({
                    path: segmentMapPoints,
                    editable: false,
                    draggable: false,
                    geodesic: true,
                    strokeColor: '#FF0000',
                    strokeOpacity: 1.0,
                    strokeWeight: 5
                })

                polyline.setMap(@map)
                @polylines.push(polyline)

                trackMapPoints.push(segmentMapPoints)

            @mapPoints.push(trackMapPoints)

    addStartFinishMarkers: ->
        # start marker
        @startMarker = new google.maps.Marker({
            position: @mapPoints[0][0][0],
            map: @map,
            title: "Start"
        })

        # finish marker
        routePoints = @mapPoints[@mapPoints.length - 1]
        trackPoints = routePoints[routePoints.length - 1]
        @finishMarker = new google.maps.Marker({
            position: trackPoints[trackPoints.length - 1],
            map: @map,
            title: "Koniec"
        })

        # add info windows
        finishInfoWindow = new google.maps.InfoWindow({
            content: "<span>Koniec</span>"
        })

        startInfoWindow = new google.maps.InfoWindow({
            content: "<span>Start</span>"
        })

        google.maps.event.addListener(@startMarker, 'click', =>
            finishInfoWindow.close()
            startInfoWindow.open(@map, @startMarker)
        )

        google.maps.event.addListener(@finishMarker, 'click', =>
            startInfoWindow.close()
            finishInfoWindow.open(@map, @finishMarker)
        )

    getRouteDistance: ->
        [distance, fullKmSectionsList] = getTotalDistance(@tracks)
        @distance = distance
        @controls.distanceDisplay.html(distance.toFixed(2))
        return fullKmSectionsList

    getStartFinishTimes: ->
        if not @tracks[0].segments[0][0].time
            return

        startTimeString = @tracks[0].segments[0][0].time
        @startTime = moment(startTimeString, 'YYYY-MM-DD HH:mm:ss')

        lastTracks = @tracks[@tracks.length-1].segments
        lastSegment = lastTracks[lastTracks.length-1]
        endTimeString = lastSegment[lastSegment.length-1].time

        @endTime = moment(endTimeString, 'YYYY-MM-DD HH:mm:ss')

        @totalTime = @endTime.diff(@startTime, 'minutes')

    drawFullKmMarkers: (fullKmSectionsList) ->
        markerCounter = 1
        for section in fullKmSectionsList
            # split section to subsections (in case section is more then km long)
            start = Math.max(Math.ceil(section.startDistance), 1)
            pt1ToFullKmDistance = start - section.startDistance

            kmsToMark = []
            while start < Math.floor(section.endDistance + 1)
                kmsToMark.push(start)
                start += 1

            # for each subsection get marker lot and lan
            i = 0
            for km in kmsToMark
                [lat, lon] = getPointOnSection(section, pt1ToFullKmDistance, i)

                # add marker to map
                latlng = new google.maps.LatLng(lat, lon)

                image = {url: "http://www.markericons.eu/ico?file=903f5ca84d5043e8998f379fe6fe8608.png&txt=#{markerCounter}km&fs=10"}

                marker = new google.maps.Marker({
                    position: latlng,
                    map: @map,
                    icon: image
                })

                @fullKmMarkers.push(marker)
                markerCounter += 1
                i += 1

    # manual route related stuff
    markers: []
    polyline: null;

    directionsService: null;
    directionsCache: {}

    mapEventHandles: [];

    initializeMapBindings: ->
        # bind to map on click event
        _this = @
        mapListenerHandle = google.maps.event.addListener(@map, 'click', (point) ->
            # add new marker to route
            _this.addMarker(point)
        )

        @mapEventHandles.push(mapListenerHandle)

    removeMapBindings: ->
        for handle in @mapEventHandles
            google.maps.event.removeListener(handle)

    addMarker: (point, position) ->
        _this = @
        marker = new google.maps.Marker({
            position: point.latLng,
            map: _this.map,
            draggable:true,
            icon: {
                path: google.maps.SymbolPath.CIRCLE,
                scale: 5
            }
        });

        # add marker to list of markers
        if position
            _this.markers.splice(position, 0, marker)
        else
            _this.markers.push(marker)

        # right click removes marker
        handle = google.maps.event.addListener(marker, 'rightclick', ->
            marker.setMap(null)
            for i in [0 .. _this.markers.length]
                if marker == _this.markers[i]
                    _this.markers.splice(i, 1)
                    break
            _this.drawManualRoute()
        )
        @mapEventHandles.push(handle)

        if @controls.useDirectionsControl.prop('checked')
            @addGoogleDirectionsRouteMarker(marker)
        else
            @addSimpleManualRouteMarker(marker)

        @drawManualRoute()

    addSimpleManualRouteMarker: (marker) ->
        # make the marker remembre not to use google directions
        marker.useGoogleDirections = false;

        _this = @
        # marker drag re-renders route
        handle = google.maps.event.addListener(marker, 'drag', ->
            _this.drawManualRoute()
        )
        @mapEventHandles.push(handle)

    addGoogleDirectionsRouteMarker: (marker) ->
        # make the marker remembre to use google directions
        marker.useGoogleDirections = true;

        _this = @

        # bind to marker drag with delay
        delay = 1000
        scrollTimeoutId = null;
        # marker drag re-renders route
        handle = google.maps.event.addListener(marker, 'drag', ->
            clearTimeout(scrollTimeoutId)
            scrollTimeoutId = setTimeout(->
                _this.drawManualRoute()
            , delay)
        )
        @mapEventHandles.push(handle)

    drawManualRoute: ->
        # remove previous polyline
        if @activePolyline
            @activePolyline.setMap(null)
            @polylines.pop()

        # escape early if there aren't enough markers to draw anything
        if @markers.length < 2
            return

        # update tracks
        path = @markersToTracks()
        if not path
            return
        else
            @tracks = path

        # draw tracks
        @drawTracks()
        fullKmSectionsList = @getRouteDistance()
        @drawFullKmMarkers(fullKmSectionsList)

        @activePolyline = @polylines[@polylines.length - 1]

        # bind click on polyline
        _this = @
        handle = google.maps.event.addListener(@activePolyline, 'click', (point) ->
            _this.polylineClickCalback(point)
        )
        @mapEventHandles.push(handle)

        @activePolyline.setMap(@map)
        @polylines.push(@activePolyline)

    polylineClickCalback: (point) ->
        # try to determin between witch two markers the line was clicked
        # how the fuck? - shortest path!
        # this might not work well with google directions
        position = getPositionOnShortestPath(@.markers, point)

        # create new marker and put it into markers list
        @.addMarker(point, position)

    getGoogleDirections: (mark1, mark2, mark3) ->
        # check directionsCache
        cacheKey = "#{mark1.position.B}:#{mark1.position.k}-#{mark2.position.B}:#{mark2.position.k}"

        path = @directionsCache[cacheKey]

        if path
            return path

        # get travel mode from controls
        travelMode = @controls.travelModeControl.find(":selected").val()

        # prepare request
        request = {
            origin: mark1.position,
            destination: mark2.position,
            travelMode: google.maps.TravelMode[travelMode]
            optimizeWaypoints: false,
            provideRouteAlternatives: false,
            region: 'pl'
        }

        # modyfy request if mark3 is given, and no path is found betwen
        # mark2 and mark3 - use route with waypoint instead of two
        # requests to google
        if mark3 and mark3.useGoogleDirections
            cacheKey2 = "#{mark2.position.B}:#{mark2.position.k}-#{mark3.position.B}:#{mark3.position.k}"
            path2 = @directionsCache[cacheKey2]

            if not (path2 and path2.length)
                request.destination = mark3.position
                waypoint = {location:mark2.position, stopover:false}
                request.waypoints = [waypoint]

        # finaly ask google
        _this = @
        @directionsService.route(request, (response, status) ->
            if status == google.maps.DirectionsStatus.OK
                # write result to local cache
                [path, path2] = _this.googleResponceToPath(response)
                _this.directionsCache[cacheKey] = path

                if path2.length
                    _this.directionsCache[cacheKey2] = path2

                # handle additional response information (google requierment)
                _this.controls.googleWarningsDisplay.html(response.routes[0].warnings)
            else if status == google.maps.DirectionsStatus.ZERO_RESULTS
                # if no path was found, (or something else went wrong)
                # set marker 2 to use straight lines instead of google
                # directions...
                mark2.useGoogleDirections = false;
                # ...and tell the user that nothing was found
                msg = "Nie znaleziono trasy - rysuję linię prostą"
                _this.controls.googleWarningsDisplay.html(msg)
            else
                # if no path was found, (or something else went wrong)
                # set marker 2 to use straight lines instead of google
                # directions
                mark2.useGoogleDirections = false;

            # re render path
            _this.drawManualRoute()
        )

        return false;

    googleResponceToPath: (response) ->
        path = []
        path2 = []

        # just to shorten some code lines
        route = response.routes[0]

        if route.legs[0].via_waypoint.length
            waypointStepIdx = route.legs[0].via_waypoint[0].step_index

            idx = 0
            for step in route.legs[0].steps
                if idx <= waypointStepIdx
                    for point in step.path
                        path.push(point)
                else
                    for point in step.path
                        path2.push(point)
                idx += 1
        else
            for point in route.overview_path
                path.push(point)

        return [path, path2]

    makeMarkersUnDragable: () ->
        for marker in @markers
            marker.setDraggable(false)

    markersToTracks: ->
        # get tracks from markers
        path = []
        i = 0
        for marker in @markers
            if not marker.useGoogleDirections or i == 0
                obj = {
                    'lat': marker.position.lat(),
                    'lon': marker.position.lng()
                }
                path.push(obj)
            else
                prevMarker = @markers[i - 1]
                nextMarker = @markers[i + 1]
                googlePath = @getGoogleDirections(prevMarker, marker, nextMarker)
                if not googlePath
                    return
                else
                    for point in googlePath
                        obj = {
                            'lat': point.lat(),
                            'lon': point.lng()
                        }
                        path.push(obj)
            i += 1

        return [{'segments': [path]}]


###############################################################################
# Distance calculations
###############################################################################

getTotalDistance = (tracks) ->
    distance = 0

    # get sections for kilometer markers
    fullKmSectionsList = []
    fullKmDistance = 0

    for track in tracks
        for segment in track['segments']
            for i in [1..segment.length - 1]
                # calculate section length
                pt1 = segment[i-1]
                pt2 = segment[i]
                x = get2PointsDistance(pt1, pt2)

                # check if full kilometer ends between section points
                if Math.floor(distance + x) > fullKmDistance
                    # save object for later marker position calculations
                    obj = {
                        startPoint: pt1
                        startDistance: distance

                        endPoint: pt2
                        endDistance: distance + x
                    }
                    fullKmSectionsList.push(obj)

                    # update variable for later checking
                    fullKmDistance = Math.floor(distance + x)

                distance += x

    return [distance, fullKmSectionsList]


get2PointsDistance = (pt1, pt2) ->
    return getDistanceFromLatLonInKm(pt1['lat'], pt1['lon'], pt2['lat'], pt2['lon'])


getPointToMarkerDistance = (obj1, obj2) ->
    if obj1.position?  # this is probably a marker
        pt1 = {'lat': obj1.position.lat(), 'lon': obj1.position.lng()}
    else  # this is probably a point
        pt1 = {'lat': obj1.latLng.lat(), 'lon': obj1.latLng.lng()}

    if obj2.position?  # this is probably a marker
        pt2 = {'lat': obj2.position.lat(), 'lon': obj2.position.lng()}
    else  # this is probably a point
        pt2 = {'lat': obj2.latLng.lat(), 'lon': obj2.latLng.lng()}

    return get2PointsDistance(pt1, pt2)


getDistanceFromLatLonInKm = (lat1, lon1, lat2, lon2) ->
    R = 6371 # Radius of the earth in km
    dlat = deg2rad(lat2-lat1)
    dlon = deg2rad(lon2-lon1)
    a = Math.sin(dlat/2) * Math.sin(dlat/2) + \
    Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) * \
    Math.sin(dlon/2) * Math.sin(dlon/2)
    c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a))
    d = R * c # Distance in km
    return d


deg2rad = (deg) ->
    return deg * (Math.PI/180)


getPositionOnShortestPath = (path, newPoint) ->
    bestDistance = 1/0
    position = null;
    for index in [1 .. path.length - 1]
        tmpPath = path.slice(0)
        tmpPath.splice(index, 0, newPoint)

        distance = 0
        for i in [1 .. tmpPath.length - 2]
            distance += getPointToMarkerDistance(tmpPath[i-1], tmpPath[i])

        if distance < bestDistance
            bestDistance = distance
            position = index
    return position


getPointOnSection = (section, pt1ToFullKmDistance, ithKilometer) ->
    deltaLon = Number(section.endPoint['lon']) - Number(section.startPoint['lon'])
    deltaLat = Number(section.endPoint['lat']) - Number(section.startPoint['lat'])

    sectionDistance = get2PointsDistance(section.startPoint, section.endPoint)
    pt1ToIthKmDistance = pt1ToFullKmDistance + ithKilometer

    lon = Math.abs(deltaLon) * pt1ToIthKmDistance / sectionDistance
    lat = Math.abs(deltaLat) * pt1ToIthKmDistance / sectionDistance

    if deltaLon < 0
        lon = lon * -1

    if deltaLat < 0
        lat = lat * -1

    return [Number(section.startPoint['lat']) + lat, Number(section.startPoint['lon']) + lon]

###############################################################################
# Expose
###############################################################################

window.RoutesMapHandler = MapHandler
