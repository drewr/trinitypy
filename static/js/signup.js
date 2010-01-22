SIGNUP = {};

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

SIGNUP.message = function(markup) {
  $("#message").html(markup);
  $("#message").show();
};

SIGNUP.submit = function(e) {
  SIGNUP.start_thinking();
  SIGNUP.do_get(this);
  SIGNUP.message("Done!  Would you like to <a href=\"\">add another</a>?");
  SIGNUP.stop_thinking();

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
