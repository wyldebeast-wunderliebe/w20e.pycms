/**
 * PyCMS inline actions and forms
 */

if (pycms === undefined) {

    var pycms = {};
}


$(document).ready(function() {

    // Handle inline actions
    // TODO: when moving to bootstrap 3.x, move to bs show event, and leave modal
    // show to bootstrap.
    $(document).on("click", "a.inline", function(e) {

        e.preventDefault();

        var action = $(e.currentTarget);
        var href = action.attr("href");

        if (href.indexOf("#") === 0) {

            // Do we have data to prefill?
            $.each(action.data("formdata") || {}, function(key, val) {
                $(href).find("[name='" + key + "']").val(val);
            });

            if ($(href).is(".modal")) {
                $(href).modal("show");
            } else {
                $(href).show();
            }
        } else {
            if (action.is(".modal")) {
                $.get(href, function(data) {
                    data.modal("show");
                });
            } else {
                $.ajax(href, {
                    data: action.data("formdata") || {},
                    type: action.data("method") || "GET",
                    success: function(data, status, xhr) {
                    }
                });
            }
        }

    });

    $(document).on("submit", "form.inline", function(e) {

        e.preventDefault();

        var form = $(e.currentTarget);
        var tgt = $(form.attr("target")) || form;

        $.ajax(form.attr("action"), {
            data: form.serialize(),
            type: form.attr("method") || "POST",
            success: function(data, status, xhr) {
                form.trigger('submit_success', [status, xhr]);
            },
            error: function(data, status, xhr) {
                form.trigger('submit_error', [status, xhr]);
            },
        });

        if (tgt.is(".modal")) {
            tgt.modal("hide");
        } else {
            tgt.hide();
        }
    });

    $(document).on("submit_success", "form.inline[action='set_password']", function(e, status, xhr) {
        // we got an error 200, but the form validation might still yield an error
        var jsonData = JSON.parse(xhr.responseText);
        if (jsonData.status != "ok") {
            pycms.alert("Password not set: " + jsonData.errors, "error");
        }
        else {
            pycms.alert("Password set", "success");
        }
    });

    $(document).on("submit_error", "form.inline[action='set_password']", function(e) {
        pycms.alert("Password not set", "error");
    });

});
