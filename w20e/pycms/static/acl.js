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
	    
	    tgt.find("form").eq(0).submit(function() {
		
		$.post($(this).attr("action"),
		       $(this).serialize(),
		       function(data) {
			   tgt.hide();
		       });
		
		return false;
	    });
	    
	    tgt.find(".cancel").click(function() {
		tgt.hide();
	    });
	});

	tgt.show();

	return false;
    });
});