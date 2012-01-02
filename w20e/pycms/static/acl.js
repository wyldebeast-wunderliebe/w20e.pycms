var pycms_acl = {};

pycms.initPartial = function(tgt) {

  tgt.find("form").eq(0).submit(function() {
      
      $.post($(this).attr("action"),
             $(this).serialize(),
             function(data) {
               
               tgt.html(data);
               
               if ($("#change_pwd_status").text() == 'ok') {
                 tgt.hide();
               } else {
                 pycms.initPartial(tgt);
               }
             });
      
      return false;
    });
  
  tgt.find(".cancel").click(function() {
      tgt.hide();
    });
}

pycms_acl.showUserAddForm = function() {
  $.get("add_user_form", {}, function(data) {
      $("#user_add_form").html(data);
      pycms.initPartial($("#user_add_form"));
    });
    $("#user_add_form").fadeIn(300);
};

pycms_acl.deleteUser = function(userId) {

  $.post("delete_user", {'user_id': userId}, function() {
      $("#" + userId).remove();      
    });
};

pycms_acl.inviteUser = function(userId) {

  $.post("invite_user", {'user_id': userId}, function() {
    $("#lbmsg").html("User invited");
    $("#lbpanel").fadeIn(300);
    $("#lb").fadeIn();
    setTimeout('$("#lb").fadeOut(300); $("#lbpanel").fadeOut(300)', 2000);
    });
};

pycms_acl.deleteKey = function(keyId) {

  $.post("delete_key", {'key': keyId}, function() {
      $("#" + keyId).remove();
    });
};


$(document).ready(function() {

    // Ajax style actions
    $(".lsaction.minimal a").click(function() {
	
        var tgt = $(this).siblings(".popup");
        
        $.get($(this).attr("href"), function(data) {
            
            tgt.html(data);
            
            pycms.initPartial(tgt);
          });
        
        tgt.show();
        
        return false;
      });
  });