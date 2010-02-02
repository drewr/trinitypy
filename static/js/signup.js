var img = function(where, id) {
  return "<img " + "id=\"" + id + "\" src=\"" + where + "\"/>";
};

SIGNUP = Object();
SIGNUP.validatable = "#email, #firstname, #lastname";
SIGNUP.validators = Object();

SIGNUP.email_pattern =
  /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;

SIGNUP.do_get = function(form){
  var q = $(form).serialize();
  console.debug($("#firstname").val());
  console.debug($("#lastname").val());
  console.debug($("#email").val());

  $.get("../tmp/foo.html?"+q, function(payload){
    console.debug(payload);
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

SIGNUP.clear_alerts = function() {
  $(SIGNUP.validatable).
    each(function(idx, el){
           var id = "#" + el.id + "_status";
           console.debug(id);
           $(id).html("");
         });
};

SIGNUP.validators.firstname = function(val) {
  return val.trim() != "";
};

SIGNUP.validators.lastname = function(val) {
  return val.trim() != "";
};

SIGNUP.validators.email = function(val) {
  console.debug("testing email " + val + ": " + SIGNUP.email_pattern.test(val));
  return SIGNUP.email_pattern.test(val);
};

SIGNUP.validate = function(idx, el) {
  var that = $(el)[0];
  var vald = SIGNUP.validators[that.id];
  var res = false;
  if (vald) {
    console.debug("validating \"" + that.id + "\"");
    // if valid, return false!
    res = SIGNUP.validators[that.id]($(that).val()) ? false : that.id;
  }
  console.debug(that.id + " is invalid: " + res);
  return res;
};

SIGNUP.any_invalid = function() {
  var res = $(SIGNUP.validatable).filter(SIGNUP.validate);
  console.debug(res);
  if (res.length == 0) {
    return false;
  }
  // some were invalid
  $(res).
    each(function(idx, el) {
           SIGNUP.alert(el.id);
         });
  return true;
};

SIGNUP.submit = function(e) {
  SIGNUP.clear_alerts();
  if (SIGNUP.any_invalid()) {
    SIGNUP.message("We found some problems.  Please fix your submission.");
  } else {
    SIGNUP.start_thinking();
    SIGNUP.do_get(this);
    SIGNUP.message("Done!  Would you like to <a href=\"\">add another</a>?");
    SIGNUP.stop_thinking();
    SIGNUP.hide_button();
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
