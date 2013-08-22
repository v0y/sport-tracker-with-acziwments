class Button
    constructor: ->
        @button = $("button")
        @button.attr('disabled', 'disabled')
        @usernameOk = @passwordOk = false

    changeButtonStatus: ->
        if @usernameOk and @passwordOk
            @button.removeAttr('disabled')
        else
            @button.attr('disabled', 'disabled')

    fieldStatus: (fieldName, isOk) ->
        # update field status. true = no errors
        switch fieldName
            when 'username' then @usernameOk = isOk
            when 'password' then @passwordOk = isOk

        # after status update enable or disable button
        @changeButtonStatus()


checkField = ($field, name, minLegth, button) ->
    if $field.val().length >= minLegth
        button.fieldStatus(name, true)
    else
        button.fieldStatus(name, false)

main = ->
    # initialize
    button = new Button
    $username = $("#id_username")
    $password = $("#id_password")

    # on document ready
    checkField($username, "username", 3, button)
    checkField($password, "password", 5, button)

    # on field change
    $username.bind("propertychange keyup paste", -> checkField($username, "username", 3, button))
    $password.bind("propertychange keyup paste", -> checkField($password, "password", 5, button))

# run
$ ->
  main()