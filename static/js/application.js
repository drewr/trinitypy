TRINITY = Object();
TRINITY.defaults = Object();
TRINITY.signup = Object();
TRINITY.url = Object();
TRINITY.url.subscribe = "/cm/subscribe/";

TRINITY.signup.do_post = function(form) {
  console.debug($(form).serialize());
  $.ajax({
           type: "post",
           url: TRINITY.url.subscribe,
           data: $(form).serialize(),
           success: function(payload, stat, req){
             console.debug(payload, stat);
             $("#email").replaceWith("<em>Thanks " + payload.email + "!</em>");
           },
           error: function(e){
             console.debug("error", e);
             $("#email").replaceWith("<em>Invalid email perhaps? <a href=\"\">Try again</a>.</em>");
           }
         });
};

TRINITY.signup.submit = function(e) {
  TRINITY.signup.do_post(this);
  return false;
};

TRINITY.init = function() {
  TRINITY.defaults.email = $("#email").val();

  $("#email")
    .focus(function(){
             if (TRINITY.defaults.email == $(this).val()) {
               $(this).val("");
             }
           });

  $("#email")
    .blur(function(){
            if ($(this).val().trim() == "") {
              $(this).val(TRINITY.defaults.email);
            }
          });

  $("#signup").submit(TRINITY.signup.submit);
};

$(document).ready(TRINITY.init);
