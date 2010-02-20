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
             $("#email").replaceWith("<div id=\"response\">" +
                                     "<em>Thanks.  We'll be in touch! " +
                                     "<a href=\"\">Add another?</a></em></div>");
           },
           error: function(e){
             console.debug("error", e);
             $("#email")
               .replaceWith("<div id=\"response\">" +
                            "<em>Invalid email address? <a href=\"\">Try again</a>.</em></div>");
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
               $(this).css("text-align", "left").val("");
             }
           });

  $("#email")
    .blur(function(){
            if ($(this).val().trim() == "") {
              $(this).css("text-align", "right").val(TRINITY.defaults.email);
            }
          });

  $("#signup form").submit(TRINITY.signup.submit);
};

$(document).ready(TRINITY.init);
