###############################################################################
# Map Handling
###############################################################################

class MapHandler
    map: null
    routes: []

    initializeMap: ->
        mapOptions = {
            center: new google.maps.LatLng(15, 15),
            zoom: 3,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        }

        @map = new google.maps.Map($("#map-canvas")[0], mapOptions)

    addRoute: (routeJson) ->
        route = new Route()
        route.tracks = routeJson
        route.map = @map
        route.draw()
        @routes.push(route)
        @getDistanceAndTimes()

    clearRoutes: ->
        for route in @routes
            route.clear()

    singleNewRoute: (routeJson) ->
        @clearRoutes()
        @addRoute(routeJson)

    getDistanceAndTimes: ->
        @distance = 0
        @startTime = @routes[0].startTime
        @endTime = @routes[0].startTime

        for route in @routes
            if route.startTime < @startTime
                @startTime = route.startTime

            if route.endTime > @endTime
                @endTime = route.endTime

            @distance += route.distance

        durationSeconds = @endTime.diff(@startTime, 'seconds')
        @duration = moment.duration(durationSeconds, 'seconds')

###############################################################################
# Route Class
###############################################################################

class Route
    map: null
    tracks: null

    polylines: []

    mapPoints: []
    distance: 0
    fullKmSectionsList: []

    startMarker: null
    finishMarker: null
    fullKmMarkers: []

    draw: ->
        @drawTracks()
        @addStartFinishMarkers()
        fullKmSectionsList = @getRouteDistance()
        @drawFullKmMarkers(fullKmSectionsList)
        @getStartFinishTimes()

    clear: ->
        for marker in @fullKmMarkers
            marker.setMap(null)

        @startMarker.setMap(null)
        @finishMarker.setMap(null)

        for polyline in @polylines
            polyline.setMap(null)

    drawTracks: ->
        # object for handling initial map zoom level and center
        latlngbounds = new google.maps.LatLngBounds()

        # add points to map
        for track in @tracks
            trackMapPoints = []
            for segment in track['segments']
                # get googl map points array
                segmentMapPoints = []
                for point in segment
                    pt = new google.maps.LatLng(point['lat'], point['lon'])
                    segmentMapPoints.push(pt)
                    latlngbounds.extend(pt)

                # create new polyline
                polyline = new google.maps.Polyline({
                    path: segmentMapPoints,
                    editable: false,
                    draggable: false,
                    geodesic: true,
                    strokeColor: '#FF0000',
                    strokeOpacity: 1.0,
                    strokeWeight: 2
                })

                polyline.setMap(@map)
                @polylines.push(polyline)

                trackMapPoints.push(segmentMapPoints)

            @mapPoints.push(trackMapPoints)

        # center / zoom map
        @map.fitBounds(latlngbounds)

    addStartFinishMarkers: ->
        # start marker
        @startMarker = new google.maps.Marker({
            position: @mapPoints[0][0][0],
            map: @map,
            title: "Start"
        })

        startInfoWindow = new google.maps.InfoWindow({
            content: "<span>Start</span>"
        })

        google.maps.event.addListener(@startMarker, 'click', ->
            finishInfoWindow.close()
            startInfoWindow.open(@map, @startMarker)
        )

        # finish marker
        routePoints = @mapPoints[@mapPoints.length - 1]
        trackPoints = routePoints[routePoints.length - 1]
        @finishMarker = new google.maps.Marker({
            position: trackPoints[trackPoints.length - 1],
            map: @map,
            title: "Koniec"
        })

        finishInfoWindow = new google.maps.InfoWindow({
            content: "<span>Koniec</span>"
        })

        google.maps.event.addListener(@finishMarker, 'click', ->
            startInfoWindow.close()
            finishInfoWindow.open(@map, @finishMarker)
        )

    getRouteDistance: ->
        [distance, fullKmSectionsList] = getTotalDistance(@tracks)
        @distance = distance
        return fullKmSectionsList

    getStartFinishTimes: ->
        startTimeString = @tracks[0].segments[0][0].time
        @startTime = moment(startTimeString, 'YYYY-MM-DD HH:mm:ss')

        lastTracks = @tracks[@tracks.length-1].segments
        lastSegment = lastTracks[lastTracks.length-1]
        endTimeString = lastSegment[lastSegment.length-1].time

        @endTime = moment(endTimeString, 'YYYY-MM-DD HH:mm:ss')

        @totalTime = @endTime.diff(@startTime, 'minutes')

    drawFullKmMarkers: (fullKmSectionsList) ->
        for section in fullKmSectionsList
            # split section to subsections (in case section is more then km long)
            start = Math.ceil(section.startDistance)
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

                marker = new google.maps.Marker({
                    position: latlng,
                    map: @map,
                    title: i + "km"
                })

                @fullKmMarkers.push(marker)


###############################################################################
# Distance calculations
###############################################################################

getTotalDistance = (routes) ->
    distance = 0

    # get sections for kilometer markers
    fullKmSectionsList = []
    fullKmDistance = 0

    for route in routes
        for segment in route['segments']
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
