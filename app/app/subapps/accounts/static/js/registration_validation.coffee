class Button
    constructor: ->
        @button = $("button")
        @button.attr('disabled', 'disabled')
        @usernameOk = @emailOk = @passwordOk = @rePasswordOk = @rules = false

    changeButtonStatus: ->
        if @usernameOk and @emailOk and @passwordOk and @rePasswordOk and @rules
            @button.removeAttr('disabled')
        else
            @button.attr('disabled', 'disabled')

    fieldStatus: (fieldName, isOk) ->
        # update field status. true = no errors
        switch fieldName
            when 'username' then @usernameOk = isOk
            when 'email' then @emailOk = isOk
            when 'password' then @passwordOk = isOk
            when 're_password' then @rePasswordOk = isOk
            when 'rules' then @rules = isOk

        # after status update enable or disable button
        @changeButtonStatus()


class Field
    constructor: (@name, @button) ->
        @field = $("#id_#{name}")
        @value = @field.val()
        @alert = $("#js-form-error-#{name}")
        @group = $("#js-#{name}-group")

    showAlert: (text) ->
        @alert.removeClass("hide").
               addClass("label-danger").
               text(text)
        @group.addClass("has-error")

    hideInfo: ->
        @alert.addClass("hide").text("")
        @group.removeClass("has-error has-success")

    setOk: ->
        @button.fieldStatus(@name, true)
        @group.removeClass("has-error").
               addClass("has-success")

    setNotOk: ->
        @button.fieldStatus(@name, false)
        @group.removeClass("has-success")

    validateMinLength: (minLength, errorText) ->
        if not @value
            @setNotOk()
        else if @value.length < minLength
            @showAlert(errorText)
            @setNotOk()
        else
            @setOk()

    validateIfNotInUse: ($field, url, errorText) ->
        ajax = $.ajax url,
            type: 'POST'
            dataType: 'html'
            data: {superCoolData: @value}
            error: (jqXHR, textStatus, errorThrown) ->
                console.log("AJAX Error: #{errorThrown}")
            success: (data, textStatus, jqXHR) ->
                if ajax.responseText is "found"
                    $field.showAlert(errorText)
                    $field.setNotOk()


class Username extends Field
    runValidators: ->
        @hideInfo()
        @value = @field.val()
        @validateMinLength(3, "Login jest zbyt krótki")

    runValidatorsOnBlur: ->
        @validateIfNotInUse(this, "/accounts/ajax/check_username", "Ten login jest już zajęty")


class Email extends Field
    constructor: ->
        super
        @emailPattern = ///^
            (?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|
            "(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*"
            )@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|
            \[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:
            (?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])
            $ ///i  # wtf is this shit?

    validateRegex: ->
        if @value.match @emailPattern
            @setOk()
        else if not @value
            @setNotOk()
        else
            @showAlert("Błędny adres e-mail")
            @setNotOk()

    runValidators: ->
        @hideInfo()
        @value = @field.val()
        @validateRegex()

    runValidatorsOnBlur: ->
        @validateIfNotInUse(this, "/accounts/ajax/check_email", "Ten email jest już zajęty")


class Password extends Field
    validateRepeat: (rePassword) ->
        if @value and rePassword.value
            if @value isnt rePassword.value
                rePassword.showAlert("Hasła nie są zgodne")
                rePassword.setNotOk()
            else
                rePassword.setOk()

    runValidators: (rePassword) ->
        @hideInfo()
        rePassword.hideInfo()
        @value = @field.val()
        @validateMinLength(5, "Hasło jest za krótkie")
        @validateRepeat(rePassword)


class RePassword extends Field
    validateRepeat: (password) ->
        if @value and password.value
            if @value isnt password.value
                @showAlert("Hasła nie są zgodne")
                @setNotOk()
            else
                @setOk()

    runValidators: (password) ->
        @hideInfo()
        @value = @field.val()
        @validateRepeat(password)


class Rules extends Field
    validateChecked: ->
        console.log(@field.is(':checked'))
        if @field.is(':checked')
            @setOk()
        else
            @setNotOk()

    runValidators: ->
        @validateChecked()

main = ->
    # initialize
    button = new Button
    username = new Username("username", button)
    email = new Email("email", button)
    password = new Password("password", button)
    rePassword = new RePassword("re_password", button)
    rules = new Rules("rules", button)

    # run validators on ready
    username.runValidators()
    email.runValidators()
    password.runValidators(rePassword)
    rePassword.runValidators(password)
    rules.runValidators()

    # run validators on fields change
    $("#id_#{username.name}").bind("propertychange keyup paste change", -> username.runValidators()).
                              on "blur", -> (username.runValidatorsOnBlur())
    $("#id_#{email.name}").bind("propertychange keyup paste change", -> email.runValidators()).
                           on "blur", -> (email.runValidatorsOnBlur())
    $("#id_#{password.name}").bind("propertychange keyup paste", -> password.runValidators(rePassword))
    $("#id_#{rePassword.name}").bind("propertychange keyup paste", -> rePassword.runValidators(password))
    $("#id_#{rules.name}").bind("click", -> rules.runValidators())

# run
$ ->
  main()
