###############################################################################
# Helpers/secondary functions
###############################################################################

changeDate = ->
    $("li.js-prev a").click (ev) ->
        ev.preventDefault()
        if not $("li.js-prev").hasClass("disabled")
            goToDate("prev")

    $("li.js-next a").click (ev) ->
        ev.preventDefault()
        if not $("li.js-next").hasClass("disabled")
            goToDate("next")


changeTimeRange = ->
    $("a.js-weight-chart-range").click (ev) ->
        ev.preventDefault()
        username = parseUrl()[0]
        timeRange = $(ev.target).data("rangeType")
        dateString = getDateString(timeRange, new Date)

        # set tab as active
        $("li[data-range-type]").removeClass("active")
        $("li[data-range-type=#{timeRange}]").addClass("active")

        refreshChart(username, timeRange, dateString)


checkChangeDateButtons = (currentDate=null, timeRange=null) ->
    # enable/disable navigation buttons
    currentDate = currentDate or new Date(getDateString("week", null, false))
    timeRange = timeRange or parseUrl()[1]
    disableClass = "disabled"

    # prev button
    $prevButton = $("li.js-prev")
    firstDate = new Date($prevButton.data("firstDate"))
    prevDate = getDateToChange(currentDate, timeRange, "prev")

    if firstDate - prevDate > currentDate - prevDate
        $prevButton.addClass(disableClass)
    else
        $prevButton.removeClass(disableClass)
    # next button
    $nextButton = $("li.js-next")
    nextDate = getDateToChange(currentDate, timeRange, "next")
    if nextDate > new Date
        $nextButton.addClass(disableClass)
    else
        $nextButton.removeClass(disableClass)


getDateString = (timeRange=null, date=null, forceMonday=true) ->
    paresedUrlList = parseUrl()
    timeRange = timeRange or paresedUrlList[1]
    if not date
        date = if timeRange == "week" and forceMonday then getLastMonday() else new Date(paresedUrlList[2])
    momentObject = moment(date)

    switch timeRange
        when "year" then momentObject.format("YYYY")
        when "month" then momentObject.format("YYYY-MM")
        when "week" then momentObject.format("YYYY-MM-DD")
        else null


getDateToChange = (currentDate, timeRange, direction) ->
    # get next date for navigation
    if direction == "prev"
        switch timeRange
            when "year" then new Date(currentDate.getFullYear()-1, 0)
            when "month" then new Date(currentDate.getFullYear(), currentDate.getMonth()-1)
            when "week" then new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate()-7)
            else null
    else if direction == "next"
        switch timeRange
            when "year" then new Date(currentDate.getFullYear()+1, 0)
            when "month" then new Date(currentDate.getFullYear(), currentDate.getMonth()+1)
            when "week" then new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate()+7)
            else null


getChartBorderDates = ->
    # get first and last day on chart

    parsedUrl = parseUrl()
    timeRange = parsedUrl[1]
    startDate = new Date(parsedUrl[2])

    switch timeRange
        when "year" then endDate = moment(startDate).endOf("year")
        when "month" then endDate = moment(startDate).endOf("month")
        when "week" then endDate = moment(startDate).endOf("week")
        else null

    [startDate, endDate]


getHumanizedDateString = (timeRange=null, dateString=null, forceMonday=true) ->
    timeRange = timeRange or parseUrl()[1]
    if not dateString
        dateString = getDateString(timeRange, new Date(dateString), forceMonday)

    switch timeRange
        when "year" then formatString = "YYYY"
        when "month" then formatString = "MMMM YYYY"
        when "week" then formatString = "D MMMM YYYY"
        else null

    moment(dateString).format(formatString)


getLastMonday = (date=null) ->
    # get last monday from date or from now
    date = date or new Date
    diff = (date.getDay() + 6) % 7  # get number of days to subtract
    new Date(date - diff * 24*60*60*1000)  # return last monday


goToDate = (direction) ->
    [username, timeRange, dateString] = parseUrl()
    currentDate = new Date(dateString)

    nextDate = getDateToChange(currentDate, timeRange, direction)
    newDateString = getDateString(timeRange, nextDate)
    refreshChart(username, timeRange, newDateString)


parseUrl = ->
    # get url without params and "http://"
    # returns [username, range type, date string yyyy-mm-dd]

    url = document.URL.split("//")[1].split("#")[0].split("/")
    [url[4], url[5], url[6]]


refreshChart = (username, timeRange, dateString) ->
        # set url
        url = "/health/show/charts/#{username}/#{timeRange}/#{dateString}"
        window.history.pushState({}, document.title, url)
        # disable navigation button?
        checkChangeDateButtons(new Date(dateString), timeRange)

        # set current date
        setDateInNavigation()

        # refresh chart
        getJsonData()


setActiveTab = ->
    timeRange = parseUrl()[1]
    $("li[data-range-type=#{timeRange}]").addClass("active")


setDateInNavigation = (dateString=null) ->
    parsedUrlList = parseUrl()
    timeRange = parsedUrlList[1]
    dateString = dateString or parsedUrlList[2]

    formattedDateString = getHumanizedDateString(timeRange, dateString)

    if timeRange == "week"
        currentDate = new Date(dateString)
        endDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate()+6)
        endDateString = getDateString("week", endDate, false)
        formattedEndDateString = getHumanizedDateString("week", endDateString, false)
        formattedDateString = "#{formattedDateString} - #{formattedEndDateString}"

    $(".js-current-date").html(formattedDateString)


###############################################################################
# Main functions
###############################################################################

getJsonData = ->
    # get json data for chart

    # get params from url
    [username, timeRange, date] = parseUrl()

    # get health data using ajax
    $.ajax
        url: "/health/api"
        type: "POST"
        dataType: "json"
        data:
            username: username
            range_type: timeRange
            date: date
            csrfmiddlewaretoken: $.cookie('csrftoken')
        error: (jqXHR, textStatus, errorThrown) -> console.log("AJAX Error: #{errorThrown}")
        success: (data) -> getChartData(data)


getChartData = (jsonData) ->
    # get data formatted for chart

    valuesForChart = {}
    for dataType, datasForType of jsonData
        valuesForChart[dataType] = []
        for data in datasForType
            splittedDate = data['x'].split("-")
            newDate = new Date(splittedDate[0], splittedDate[1]-1, splittedDate[2])
            valuesForChart[dataType].push {'x': newDate, 'y': data['y']}

    chartData = [
        {
            color: "#61AE24"
            key: "Waga (kg)"
            values: valuesForChart.weight
        },
        {
            color: "#F18D05"
            key: "Tłuszcz (%)"
            values: valuesForChart.fat
        },
        {
            color: "#00A1CB"
            key: "Woda (%)"
            values: valuesForChart.water
        },
    ]

    nv.addGraph(chartData)


nv.addGraph = (chartData) ->
    # chow chart
    chart = nv.models.lineChart()
        .useInteractiveGuideline(true)
        .margin({bottom: 70, left: 75})
        .forceX(getChartBorderDates())

    chart.xAxis
        .axisLabel("Data")
        .rotateLabels(-30)
        .tickFormat (d) ->
            d3.time.format("%d-%m-%Y")(new Date(d))

    chart.yAxis
        .axisLabel("Wartość")
        .tickFormat(d3.format(",.1f"))

    $chart = d3.select(".weight-chart svg")

    $chart
        .datum(chartData)
        .transition().duration(500).call(chart)

    nv.utils.windowResize -> $chart.call(chart)

    chart


###############################################################################
# Run
###############################################################################

$ ->
    moment.lang("pl")         # set moment's language
    setActiveTab()            # set as active right tab
    changeTimeRange()         # change time range tab
    changeDate()              # Change date to prev/next
    checkChangeDateButtons()  # enable/disable navigation buttons
    setDateInNavigation()     # show current view date
    getJsonData()             # get data and draw chart
