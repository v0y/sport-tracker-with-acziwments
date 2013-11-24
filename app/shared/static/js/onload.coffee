$ ->
    # tooltip
    $(".js-tooltip").tooltip()

    # datepicker
    $(".input-append.date").datepicker({
        format: "dd-mm-yyyy",
        todayBtn: "linked",
        language: "pl",
        forceParse: false,
        todayHighlight: true,
        autoclose: true
    })
