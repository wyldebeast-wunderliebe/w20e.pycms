/**
 * Pycms inline editing JS lib.
 */

if (pycms == undefined) {
    var pycms = {};
}


$(document).ready(function() {

    $(document).on("submit", ".modal form", function(e) {

        var form = $(e.target);
        var modal = form.parents(".modal");

        $.post(form.attr("action"),
               form.serialize(),
               function(data, status, xhr) {

                 if (xhr.status == 200) {
                   pycms.alert("ok", "success");
                   modal.modal("hide");
                   $(document).triggerHandler("ie_changed", [data]);
                 } else if (xhr.status >= 300 && xhr.status < 400) {
                   pycms.alert("Something went wrong...", "error");
                   modal.modal("hide");
                 } else {
                   modal.find(".modal-body").html(data);
                 }

               })
          
          e.preventDefault();
          return false;
      });

    $(document).on("click", ".rm-inline", function(e) {
        var link = $(e.currentTarget);

        $.post(link.attr("href"), function(data, status, xhr) {
            if (xhr.status == 200) {
              $(document).triggerHandler("ie_changed", [data]);
            } else {
              pycms.alert("Something went wrong...", "error");
            }
          });

        e.preventDefault();
      });
  });
