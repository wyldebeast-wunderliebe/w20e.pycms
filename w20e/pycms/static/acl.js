/** 
 * Security related functions for PyCMS.
 */

if (pycms == undefined) {
  var pycms = {};
}

pycms.acl = {};

/**
 * Add user AJAX style and if successful, add to view.
 */
pycms.acl.addUser = function() {

  $.ajax({"url": "add_user", 
          "type": "POST",
          "data": $("#user_add_form form").serialize(),
          "success": function(data) {
        if (data['status'] == "error") {
          $("#user_add_alert").html(data['errmsg']);
          $("#user_add_alert").show();
        } else {
          var tr = $("#userlisting tr").last().clone();
          tr.attr("data-userid", data['user']['id']);
          tr.find("td").eq(2).html(data['user']['id']);
          tr.find("td").eq(3).html(data['user']['name']);
          tr.find("td").eq(4).html(data['user']['email']);
          $("#userlisting").append(tr);
          pycms.acl.initActions(tr);
          $("#user_add_form").modal('hide');
        }
      },
          "error": function(data) {}
    });
}

pycms.acl.showUserAddForm = function() {
  $("#user_add_form").modal();
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

pycms.acl.initActions = function(row) {

  var elts;
  
  if (row) {
    elts = row.find(".btn.delete");
  } else {
    elts = $(".btn.delete");
  }

  elts.click(function() {
      
      try {
        var tr = $(this).parents("tr").first();
        var userId = tr.attr("data-userid");
        pycms.acl.deleteUser(userId);
        tr.remove();
      } catch (e) {
        console.log(e);
      }
      
      return false;
    });
}

$(document).ready(function() {

    pycms.acl.initActions();
  });