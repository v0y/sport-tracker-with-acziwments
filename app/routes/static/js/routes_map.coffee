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
# Distance calculations
###############################################################################

getTotalDistance = (routes) ->
    distance = 0

    for route in routes
        for segment in route['segments']
            for i in [1..segment.length - 1]
                pt1 = segment[i-1]
                pt2 = segment[i]
                x = getDistanceFromLatLonInKm(pt1['lat'], pt1['lon'], pt2['lat'], pt2['lon'])
                distance += x

    return distance


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

displayRoutesDistance = (routesJSON) ->
    distance = getTotalDistance(routesJSON)
    distance = Math.round(distance * 100) / 100
    $("#total-distance").html(distance + " km")

###############################################################################
# Run
###############################################################################

window.main = (routesJSON) ->
    if not $.isEmptyObject(routesJSON)
        # intialize map
        map = initializeMap()
        # draw routes on map
        drawRoutes(routesJSON, map)
        # get distance related data
        displayRoutesDistance(routesJSON)
