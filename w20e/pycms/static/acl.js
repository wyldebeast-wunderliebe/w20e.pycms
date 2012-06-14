if (pycms == undefined) {
  var pycms = {};
}

pycms.acl = {};

pycms.acl.addUser = function() {
  $.post("add_user", data,
         function() {
         });
}

pycms.acl.showUserAddForm = function() {
      $("#user_add_form").modal();
    });
};

pycms.acl.deleteUser = function(userId) {

  $.post("delete_user", {'user_id': userId}, function() {
      $("#" + userId).remove();      
    });
};

pycms.acl.inviteUser = function(userId) {

  $.post("invite_user", {'user_id': userId}, function() {
    $("#lbmsg").html("User invited");
    $("#lbpanel").fadeIn(300);
    $("#lb").fadeIn();
    setTimeout('$("#lb").fadeOut(300); $("#lbpanel").fadeOut(300)', 2000);
    });
};

pycms.acl.deleteKey = function(keyId) {

  $.post("delete_key", {'key': keyId}, function() {
      $("#" + keyId).remove();
    });
};
