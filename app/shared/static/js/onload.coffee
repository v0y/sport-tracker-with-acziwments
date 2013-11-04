$ ->
    # tooltip
    $("[rel=tooltip]").tooltip()

    # datepicker
    $(".datepicker-button").datepicker({
        format: "dd-mm-yyyy",
        todayBtn: "linked",
        language: "pl",
        forceParse: false,
        todayHighlight: true
    })
