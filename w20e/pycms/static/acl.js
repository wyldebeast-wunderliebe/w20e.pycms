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
          tr.data("userid", data['user']['id']);
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
};

/**
 * Store groups for user
 */
pycms.acl.setUserGroups = function() {
    $.post("user_groups", $("#user_groups form").serialize(),
            function(data) {
                $("#user_groups").modal('hide');
            });
}

pycms.acl.showUserAddForm = function() {
  $("#user_add_form").modal();
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

  /* BIND SET USER-GROUPS BUTTON */

  if (row) {
    elts = row.find(".btn.set_user_groups");
  } else {
    elts = $(".btn.set_user_groups");
  }

  elts.click(function(e) {
      e.preventDefault();
      var tr = $(this).parents("tr").first();
      var userid = tr.data('userid');
      var url = "user_groups";

      /* load the form with ajax */
      $.ajax({
          url: url,
          data: {user_id: userid},
          success: function(data){
              // first remove old user_groups modal form
              $("#user_groups").remove();
              $(data).modal('show');
          },
          cache: false
      });
  });
}

$(document).ready(function() {

    pycms.acl.initActions();
  });
