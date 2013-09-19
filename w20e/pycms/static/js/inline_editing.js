/**
 * Inline editing
 */

// pu_in namespace
if (ie == undefined) {
  var ie = {};
}


// Hold current action
ie.CURRENTACTION = null;


/**
 * Handle action result.
 * @param elt Element that triggered the action
 * @param data Result data
 * @param status Response status
 * @param xhr Result XHR
 */
ie.handleData = function(tgt, data, behavior) {

  if (tgt) {
    if (behavior == "replace") {
      tgt.replaceWith(data);
    } else if (behavior == "append") {
      tgt.append(data);
    } else if (behavior == "prepend") {
      tgt.prepend(data);
    } else if (behavior == "remove") {
      tgt.remove();
    } else {
      tgt.html(data);
    }
  }

  if (ie.CURRENTACTION.data("protect")) {
    ie.CURRENTACTION.removeClass("disabled");
  }
};


// Initialize ie event handlers.
//
$(document).ready(function() {

    $(document).on("click", ".add-inline", function(e) {

        ie.CURRENTACTION = $(e.currentTarget);
      });

    $(document).on("click", ".edit-inline", function(e) {

        ie.CURRENTACTION = $(e.currentTarget);
      });

    $(document).on("click", ".rm-inline", function(e) {
        ie.CURRENTACTION = $(e.currentTarget);
      });

    $(document).on("ie_changed", function(e, data) {

        if (ie.CURRENTACTION) {
          if (ie.CURRENTACTION.hasClass("add-inline")) {

            var model = ie.CURRENTACTION.data("model") ||             
              ie.CURRENTACTION.parents(".ie-container").data("model");
          
            $(document).triggerHandler("ie_add_object", [model, data]);
          }
          if (ie.CURRENTACTION.hasClass("rm-inline")) {

            var model = ie.CURRENTACTION.data("model") ||             
              ie.CURRENTACTION.parents(".ie-container").data("model");
          
            $(document).triggerHandler("ie_rm_object", [model, data]);
          }
        }

        ie.CURRENTACTION = null;
      });

    $(document).on("ie_add_object", function(e, model, data) {
        $(".ie-container[data-model=" + model + "]").each(function() {
            ie.handleData($(this), data, $(this).data("behaviour") || "append");
          });
      });

    $(document).on("ie_rm_object", function(e, model, data) {

        var objId = ie.CURRENTACTION.data("objid");

        $(".ie-container[data-model=" + model + "]").each(function() {

            $(this).find("[data-objid=" + objId + "]").parents(".ie-object").remove();
          });
      });
  });
