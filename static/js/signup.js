var img = function(where, id) {
  return "<img " + "id=\"" + id + "\" src=\"" + where + "\"/>";
};

SIGNUP = Object();
SIGNUP.validators = Object();

SIGNUP.email_pattern =
  /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;

SIGNUP.do_get = function(form){
  var q = $(form).serialize();
  console.log($("#firstname").val());
  console.log($("#lastname").val());
  console.log($("#email").val());

  $.get("../tmp/foo.html?"+q, function(payload){
    console.log(payload);
  });

};

SIGNUP.sleep = function(delay) {
};

SIGNUP.start_thinking = function() {
  $("#thinking").show();
};

SIGNUP.stop_thinking = function() {
  $("#thinking").hide();
};

SIGNUP.hide_message = function() {
  $("#message").hide();
};

SIGNUP.hide_button = function() {
  $("tr > td > input#signupsubmit").hide();
};

SIGNUP.message = function(markup) {
  $("#message").html(markup);
  $("#message").show();
};

SIGNUP.alert = function(field) {
  var id = "#" + field + "_status";
  $(id).html(img("../static/img/alert.gif"));
};

SIGNUP.validators.email = function(val) {
  return SIGNUP.email_pattern.test(val);
};

SIGNUP.validate = function() {
  var vald = SIGNUP.validators[this.id];
  if (vald) {
    console.log("validating \"" + this.id + "\"");
    return SIGNUP.validators[this.id]($(this).val());
  } else {
    return false;
  }
};

SIGNUP.is_valid = function () {
  $(":input").map(SIGNUP.validate);
  return true;
};

SIGNUP.submit = function(e) {
  if (SIGNUP.is_valid()) {
    SIGNUP.start_thinking();
    SIGNUP.do_get(this);
    SIGNUP.message("Done!  Would you like to <a href=\"\">add another</a>?");
    SIGNUP.stop_thinking();
    SIGNUP.hide_button();
  } else {
    SIGNUP.message("We found some problems.  Please fix your submission.");
    SIGNUP.alert("email");
  }

  console.debug("form submitted");
  return false;
};

SIGNUP.init = function() {
  SIGNUP.hide_message();
  SIGNUP.stop_thinking();
  $("#signupform").submit(SIGNUP.submit);
};

$(document).ready(function(){
  console.debug("JS loaded");
  SIGNUP.init();
});
