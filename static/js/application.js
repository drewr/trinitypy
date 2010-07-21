TRINITY = Object();
TRINITY.defaults = Object();
TRINITY.signup = Object();
TRINITY.nav = Object();
TRINITY.url = Object();
TRINITY.url.subscribe = "/cm/subscribe/";

TRINITY.signup.do_post = function(form) {
  $.ajax({
           type: "post",
           url: TRINITY.url.subscribe,
           data: $(form).serialize(),
           success: function(payload, stat, req){
             $("#email").replaceWith("<div id=\"response\">" +
                                     "<em>Thanks.  We'll be in touch! " +
                                     "<a href=\"\">Add another?</a></em></div>");
           },
           error: function(e){
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

TRINITY.nav.expire_hover = function () {
  if (TRINITY.nav.menu) {
    TRINITY.nav.menu.find("ul").fadeOut("fast");
  }
};

TRINITY.nav.on = function() {
  if (TRINITY.nav.menu) {
    TRINITY.nav.menu.find("ul").fadeOut("fast");
    TRINITY.nav.menu = null;
  }
  $(this).find("ul").show();
};

TRINITY.nav.off = function() {
  TRINITY.nav.menu = $(this);
  setTimeout("TRINITY.nav.expire_hover()", 50);
};

TRINITY.nav.set_up = function() {
  TRINITY.nav.menu = null;
  $("#nav > ul > li").hover(TRINITY.nav.on, TRINITY.nav.off);
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

  TRINITY.nav.set_up();
};

$(document).ready(TRINITY.init);
