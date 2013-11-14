###############################################################################
# Map Handling
###############################################################################

initializeMap = ->
    mapOptions = {
        center: new google.maps.LatLng(15, 15),
        zoom: 3,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    }

    return new google.maps.Map($("#map-canvas")[0], mapOptions)


drawRoutes = (routes, map) ->
    # object for handling initial map zoom level and center
    latlngbounds = new google.maps.LatLngBounds()

    # add points to map
    for route in routes
        for segment in route['segments']
            # get googl map points array
            mapPoints = []
            for point in segment
                pt = new google.maps.LatLng(point['lat'], point['lon'])
                mapPoints.push(pt)
                latlngbounds.extend(pt)

            # create new polyline
            polyline = new google.maps.Polyline({
                path: mapPoints,
                editable: false,
                draggable: false,
                geodesic: true,
                strokeColor: '#FF0000',
                strokeOpacity: 1.0,
                strokeWeight: 2
            })

            polyline.setMap(map)

    addStartFinishMarkers(mapPoints, map)

    # center / zoom map
    map.fitBounds(latlngbounds)


addStartFinishMarkers = (mapPoints, map) ->
    # start marker
    startMarker = new google.maps.Marker({
        position: mapPoints[0],
        map: map,
        title: "Start"
    })

    startInfoWindow = new google.maps.InfoWindow({
        content: "<span>Start</span>"
    })

    google.maps.event.addListener(startMarker, 'click', ->
        finishInfoWindow.close()
        startInfoWindow.open(map, startMarker)
    )

    # finish marker
    finishMarker = new google.maps.Marker({
        position: mapPoints[mapPoints.length - 1],
        map: map,
        title: "Koniec"
    })

    finishInfoWindow = new google.maps.InfoWindow({
        content: "<span>Koniec</span>"
    })

    google.maps.event.addListener(finishMarker, 'click', ->
        startInfoWindow.close()
        finishInfoWindow.open(map, finishMarker)
    )


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


drawFullKmMarkers = (fullKmSectionsList, map) ->
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
                map: map,
                title: i + "km"
            })


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


displayRoutesDistance = (routesJSON, map) ->
    [distance, fullKmSectionsList] = getTotalDistance(routesJSON)
    distance = Math.round(distance * 1000) / 1000
    $("#total-distance").html(distance + " km")
    drawFullKmMarkers(fullKmSectionsList, map)

###############################################################################
# Run
###############################################################################

window.main = (routesJSON) ->
    if not $.isEmptyObject(routesJSON)
        # intialize map
        map = initializeMap()
        # draw routes on map
        drawRoutes(routesJSON, map)
        # display distance related data
        displayRoutesDistance(routesJSON, map)
