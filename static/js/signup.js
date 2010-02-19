var img = function(where, id) {
  return "<img " + "id=\"" + id + "\" src=\"" + where + "\"/>";
};

SIGNUP = Object();
SIGNUP.validatable = "#email, #firstname, #lastname";
SIGNUP.validators = Object();
SIGNUP.url = Object();
SIGNUP.url.subscribe = "/cm/subscribe/";
SIGNUP.url.alert_gif = "img/alert.gif";

SIGNUP.email_pattern =
  /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;

SIGNUP.do_post = function(form){
  $.ajax({
           type: "post",
           url: SIGNUP.url.subscribe,
           data: $(form).serialize(),
           success: function(payload, stat, req){
             console.debug(payload, stat);
             if (payload.result == "success") {
               SIGNUP.hide_button();
               SIGNUP.message("Done!  Would you like to <a href=\"\">add another</a>?");
             } else {
               SIGNUP.message("Something went wrong.  Try again.");
             }
           },
           error: function(e){
             console.debug("error");
             SIGNUP.message("The network had a problem.  Try again.");
           }
         });
};

SIGNUP.setup_thinking = function() {
  $("#thinking").hide();
  $("#thinking").
    ajaxStart(function(){
                $(this).show();
              });
  $("#thinking").
    ajaxStop(function(){
                $(this).hide();
              });
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
  $(id).html(img(SIGNUP.url.alert_gif));
};

SIGNUP.clear_alerts = function() {
  $(SIGNUP.validatable).
    each(function(idx, el){
           var id = "#" + el.id + "_status";
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
  return SIGNUP.email_pattern.test(val);
};

SIGNUP.validate = function(idx, el) {
  var that = $(el)[0];
  var vald = SIGNUP.validators[that.id];
  var res = false;
  if (vald) {
    // if valid, return false!
    res = SIGNUP.validators[that.id]($(that).val()) ? false : that.id;
  }
  console.debug(that.id + " is invalid: " + res);
  return res;
};

SIGNUP.any_invalid = function() {
  var res = $(SIGNUP.validatable).filter(SIGNUP.validate);
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
    return false;
  }

  SIGNUP.do_post(this);
  console.debug("form submitted");
  return false;
};

SIGNUP.init = function() {
  console.debug("SIGNUP loaded");
  SIGNUP.hide_message();
  SIGNUP.setup_thinking();
  $("#signupform").submit(SIGNUP.submit);
};

$(document).ready(SIGNUP.init);
