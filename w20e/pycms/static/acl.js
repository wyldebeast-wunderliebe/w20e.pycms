var pycms_acl = {};

pycms_acl.showUserAddForm = function() {
    $("#user_add_form").load("add_user_form");
    $("#lbpanel").fadeIn(300);
    $("#user_add_form").fadeIn(300);
};

pycms_acl.addUser = function() {
  var data = $("#user_add_form form").serialize();
  
  data += '&submit=1';

  $.post("add_user_form", data, function() {
    $("#user_add_form").hide();
    $("#lbmsg").html("User added");
    $("#lb").fadeIn();
    setTimeout('$("#lb").fadeOut(300); $("#lbpanel").fadeOut(300)', 2000);
    });
};

pycms_acl.deleteUser = function(userId) {

  $.post("delete_user", {'user_id': userId}, function() {
    $("#lbmsg").html("User deleted");
    $("#lbpanel").fadeIn(300);
    $("#lb").fadeIn();
    setTimeout('$("#lb").fadeOut(300); $("#lbpanel").fadeOut(300)', 2000);
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

