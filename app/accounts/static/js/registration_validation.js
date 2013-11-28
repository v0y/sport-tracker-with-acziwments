// Generated by CoffeeScript 1.6.3
(function() {
  var Button, Email, Field, Password, RePassword, Rules, Username, main, _ref, _ref1, _ref2,
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  Button = (function() {
    function Button() {
      this.button = $("button");
      this.button.attr('disabled', 'disabled');
      this.usernameOk = this.emailOk = this.passwordOk = this.rePasswordOk = this.rules = false;
    }

    Button.prototype.changeButtonStatus = function() {
      if (this.usernameOk && this.emailOk && this.passwordOk && this.rePasswordOk && this.rules) {
        return this.button.removeAttr('disabled');
      } else {
        return this.button.attr('disabled', 'disabled');
      }
    };

    Button.prototype.fieldStatus = function(fieldName, isOk) {
      switch (fieldName) {
        case 'username':
          this.usernameOk = isOk;
          break;
        case 'email':
          this.emailOk = isOk;
          break;
        case 'password':
          this.passwordOk = isOk;
          break;
        case 're_password':
          this.rePasswordOk = isOk;
          break;
        case 'rules':
          this.rules = isOk;
      }
      return this.changeButtonStatus();
    };

    return Button;

  })();

  Field = (function() {
    function Field(name, button) {
      this.name = name;
      this.button = button;
      this.field = $("#id_" + name);
      this.value = this.field.val();
      this.alert = $("#js-form-error-" + name);
      this.group = $("#js-" + name + "-group");
    }

    Field.prototype.showAlert = function(text) {
      this.alert.removeClass("hidden").addClass("label-danger").text(text);
      return this.group.addClass("has-error");
    };

    Field.prototype.hideInfo = function() {
      this.alert.addClass("hidden").text("");
      return this.group.removeClass("has-error has-success");
    };

    Field.prototype.setOk = function() {
      this.button.fieldStatus(this.name, true);
      this.group.removeClass("has-error").addClass("has-success");
      return true;
    };

    Field.prototype.setNotOk = function() {
      this.button.fieldStatus(this.name, false);
      this.group.removeClass("has-success");
      return false;
    };

    Field.prototype.validateMinLength = function(minLength, errorText) {
      if (!this.value) {
        return this.setNotOk();
      } else if (this.value.length < minLength) {
        this.showAlert(errorText);
        return this.setNotOk();
      } else {
        return this.setOk();
      }
    };

    Field.prototype.validateIfNotInUse = function($field, url, errorText) {
      var ajax;
      return ajax = $.ajax(url, {
        type: 'POST',
        dataType: 'html',
        data: {
          superCoolData: this.value,
          csrfmiddlewaretoken: $.cookie('csrftoken')
        },
        error: function(jqXHR, textStatus, errorThrown) {
          return console.log("AJAX Error: " + errorThrown);
        },
        success: function(data, textStatus, jqXHR) {
          if (ajax.responseText === "found") {
            $field.showAlert(errorText);
            return $field.setNotOk();
          }
        }
      });
    };

    Field.prototype.validateRegex = function(pattern, alertText) {
      if (this.value.match(pattern)) {
        return this.setOk();
      } else if (!this.value) {
        return this.setNotOk();
      } else {
        this.showAlert(alertText);
        return this.setNotOk();
      }
    };

    return Field;

  })();

  Username = (function(_super) {
    __extends(Username, _super);

    function Username() {
      Username.__super__.constructor.apply(this, arguments);
      this.usernamePattern = /^[\w.@+-]+$/i;
    }

    Username.prototype.runValidators = function() {
      var isOk;
      this.hideInfo();
      this.value = this.field.val();
      isOk = this.validateMinLength(3, "Login jest zbyt krótki");
      if (isOk) {
        return this.validateRegex(this.usernamePattern, "Login może zawierać tylko litery, cyfry i znaki _ + @ .-");
      }
    };

    Username.prototype.runValidatorsOnBlur = function() {
      return this.validateIfNotInUse(this, "/accounts/api/check_username", "Ten login jest już zajęty");
    };

    return Username;

  })(Field);

  Email = (function(_super) {
    __extends(Email, _super);

    function Email() {
      Email.__super__.constructor.apply(this, arguments);
      this.emailPattern = /^(?:[a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])$/i;
    }

    Email.prototype.runValidators = function() {
      this.hideInfo();
      this.value = this.field.val();
      return this.validateRegex(this.emailPattern, "Podaj poprawny adres email");
    };

    Email.prototype.runValidatorsOnBlur = function() {
      return this.validateIfNotInUse(this, "/accounts/api/check_email", "Ten email jest już zajęty");
    };

    return Email;

  })(Field);

  Password = (function(_super) {
    __extends(Password, _super);

    function Password() {
      _ref = Password.__super__.constructor.apply(this, arguments);
      return _ref;
    }

    Password.prototype.validateRepeat = function(rePassword) {
      if (this.value && rePassword.value) {
        if (this.value !== rePassword.value) {
          rePassword.showAlert("Hasła nie są zgodne");
          return rePassword.setNotOk();
        } else {
          return rePassword.setOk();
        }
      }
    };

    Password.prototype.runValidators = function(rePassword) {
      this.hideInfo();
      rePassword.hideInfo();
      this.value = this.field.val();
      this.validateMinLength(5, "Hasło jest za krótkie");
      return this.validateRepeat(rePassword);
    };

    return Password;

  })(Field);

  RePassword = (function(_super) {
    __extends(RePassword, _super);

    function RePassword() {
      _ref1 = RePassword.__super__.constructor.apply(this, arguments);
      return _ref1;
    }

    RePassword.prototype.validateRepeat = function(password) {
      if (this.value && password.value) {
        if (this.value !== password.value) {
          this.showAlert("Hasła nie są zgodne");
          return this.setNotOk();
        } else {
          return this.setOk();
        }
      }
    };

    RePassword.prototype.runValidators = function(password) {
      this.hideInfo();
      this.value = this.field.val();
      return this.validateRepeat(password);
    };

    return RePassword;

  })(Field);

  Rules = (function(_super) {
    __extends(Rules, _super);

    function Rules() {
      _ref2 = Rules.__super__.constructor.apply(this, arguments);
      return _ref2;
    }

    Rules.prototype.validateChecked = function() {
      if (this.field.is(':checked')) {
        return this.setOk();
      } else {
        return this.setNotOk();
      }
    };

    Rules.prototype.runValidators = function() {
      this.validateChecked();
      return true;
    };

    return Rules;

  })(Field);

  main = function() {
    var button, email, password, rePassword, rules, username;
    button = new Button;
    username = new Username("username", button);
    email = new Email("email", button);
    password = new Password("password", button);
    rePassword = new RePassword("re_password", button);
    rules = new Rules("rules", button);
    username.runValidators();
    email.runValidators();
    password.runValidators(rePassword);
    rePassword.runValidators(password);
    rules.runValidators();
    $("#id_" + username.name).bind("propertychange keyup paste change", function() {
      return username.runValidators();
    }).on("blur", function() {
      return username.runValidatorsOnBlur();
    });
    $("#id_" + email.name).bind("propertychange keyup paste change", function() {
      return email.runValidators();
    }).on("blur", function() {
      return email.runValidatorsOnBlur();
    });
    $("#id_" + password.name).bind("propertychange keyup paste", function() {
      return password.runValidators(rePassword);
    });
    $("#id_" + rePassword.name).bind("propertychange keyup paste", function() {
      return rePassword.runValidators(password);
    });
    return $("#id_" + rules.name).bind("click", function() {
      return rules.runValidators();
    });
  };

  $(function() {
    return main();
  });

}).call(this);
