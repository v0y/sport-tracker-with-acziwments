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

    # center / zoom map
    map.fitBounds(latlngbounds)

###############################################################################
# Run
###############################################################################

window.main = (routesJSON) ->
    if not $.isEmptyObject(routesJSON)
        # intialize map
        map = initializeMap()
        # draw routes on map
        drawRoutes(routesJSON, map)
