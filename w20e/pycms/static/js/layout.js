/**
 * Pycms inline editing JS lib.
 */

if (pycms == undefined) {
    var pycms = {};
}


/**
 * Pycms inline editing namespace
 */
pycms.ie = {
  TEMPLATES: {},
  OBJECTMAP: {},
  OBJECTS: {},
  CONTAINERS: {}
};


/**
 * Add object to local objects.
 * @param model Model type
 * @param obj Created object
 */
pycms.ie.addObject = function(model, obj) {

  if (!pycms.ie.OBJECTMAP[model]) {
    pycms.ie.OBJECTMAP[model] = {};
  }

  if (!pycms.ie.OBJECTS[model]) {
    pycms.ie.OBJECTS[model] = 0;
  }

  if (!obj.id) {
    obj.id = model + "_" + pycms.ie.OBJECTS[model];
  }

  pycms.ie.OBJECTS[model]++;
  pycms.ie.OBJECTMAP[model][obj.id] = obj;

  return obj;
};


/**
 * Remove object for the given model and id.
 * @param model Model for object
 * @param id Object id
 */
pycms.ie.rmObject = function(model, id) {

  delete pycms.ie.OBJECTMAP[model][id];
  pycms.ie.OBJECTS[model]--;
};


/**
 * Update object for the given model and object. Object should have id.
 * @param model Model for object
 * @param obj Object
 */
pycms.ie.updateObject = function(model, obj) {

  pycms.ie.OBJECTMAP[model][obj.id] = obj;
};


/**
 * Get the object specified by it's id
 * @param model Model to fetch
 * @param id Object id
 */
pycms.ie.getObject = function(model, id) {
  
  return pycms.ie.OBJECTMAP[model][id];
};


/**
 * Get all objects for model
 * @param model Model to fetch
 */
pycms.ie.getObjects = function(model) {

  objects = []

  for (key in pycms.ie.OBJECTMAP[model]) {
    objects.push(pycms.ie.OBJECTMAP[model][key])
  }

  return objects;
};


/**
 * Render a template using underscore.
 * @param model Model to get template for
 * @param mode Template mode. Usually one of edit, add or view
 * @param data Dict of data
 */
pycms.ie.renderTemplate = function(model, mode, data){
     
  return _.template(pycms.ie.TEMPLATES[model][mode], data);
};


/**
 * Convert form to dict
 * @param form jQuery wrapped form object
 */
pycms.ie.formAsDict = function(form) {

  data = {};
  formdata = form.serializeArray();

  for (var i = 0; i < formdata.length; i++) {
    data[formdata[i].name] = formdata[i].value;
  }

  return data;
};


/**
 * Apply dict to form
 * @param dict Associative array with values
 * @param form jQuery wrapped form object
 */
pycms.ie.dictAsForm = function(dict, form) {

  for (key in dict) {

    form.find("[name='" + key + "']").val(dict[key]);
  }
};


/**
 * Serialize the instances of the given model to JSON.
 * @param model Model
 */
pycms.ie.serializeObjects = function(model) {

  return JSON.stringify(pycms.ie.getObjects(model));
};


/**
 * Update all containers for given model with the snippet.
 * @param model Model
 * @param snippet HTML snippet to use
 * @param id Id of object. If provided, replace, otherise add
 */
pycms.ie.updateContainers = function(model, snippet, id) {

  if (!id) {
    for (var i = 0; i < pycms.ie.CONTAINERS[model].length; i++) {
      pycms.ie.CONTAINERS[model][i].append(snippet);
    }
  } else {
    for (var i = 0; i < pycms.ie.CONTAINERS[model].length; i++) {
      pycms.ie.CONTAINERS[model][i].find("[data-object_id='" + id + "']").
      replaceWith(snippet);
    }
  }
};


$(document).ready(function() {

    // Append form container
    $("body").append('<div id="pycms_ie_form"></div>');

    // Load templates
    $("link[rel='template']").each(function() {

        var link = $(this);

        $.get(link.attr("href"), function(data) {

            if (!pycms.ie.TEMPLATES[link.data("model")]) {
              pycms.ie.TEMPLATES[link.data("model")] = [];
            }
           
            pycms.ie.TEMPLATES[link.data("model")][link.data("mode")] = data;

            $(document).triggerHandler("pycms_ie_template_loaded", [data]);
          });
      });

    // Find all containers and set up model stuff.
    $(".pycms_ie_addable").each(function() {

        var model = $(this).data("model");

        if (!pycms.ie.CONTAINERS.model) {
          pycms.ie.CONTAINERS[model] = [];
        }

        pycms.ie.CONTAINERS[model].push($(this));
      });

    $(document).on("click", ".pycms_ie_rm", function(e) {
        var link = $(e.currentTarget);
        var rec = link.parents(".pycms_ie_editable").eq(0);

        pycms.ie.rmObject(rec.data("model"), rec.data("object_id"));

        $(document).triggerHandler("pycms_ie_rm_object", 
                                   [rec.data("model"), 
                                    rec.data("object_id")]);

        rec.remove();
      });

    $(document).on("click", ".pycms_ie_edit", function(e) {
        var link = $(e.currentTarget);
        var rec = link.parents(".pycms_ie_editable").eq(0);
        var model = rec.data("model");

        var obj = pycms.ie.getObject(model, rec.data("object_id"));

        $("#pycms_ie_form").css("left", link.offset().left - 100);
        $("#pycms_ie_form").css("top", link.offset().top);
        $("#pycms_ie_form").html(pycms.ie.renderTemplate(model, "edit", obj));
        $("#pycms_ie_form form").data("model", model);
        $("#pycms_ie_form form").data("object_id", obj.id);

        pycms.ie.dictAsForm(obj, $("#pycms_ie_form form"));

        $("#pycms_ie_form").show();

        e.preventDefault();
      });

    $(".pycms_ie_objects").each(function() {

        var objects = JSON.parse($(this).val());
        var model = $(this).data("model");

        for (var i= 0; i < objects.length; i++) {
          pycms.ie.addObject(model, objects[i]);
        }
      });

    $(".pycms_ie_add_object").click(function(e) {

        var link = $(e.currentTarget);
        var model = link.data("model");

        $("#pycms_ie_form").css("left", link.offset().left);
        $("#pycms_ie_form").css("top", link.offset().top);
        $("#pycms_ie_form").html(pycms.ie.renderTemplate(model, "add", {}));

        $("#pycms_ie_form form").data("model", model);

        $("#pycms_ie_form").show();

        e.preventDefault();
      });

    $(document).on("submit", "#pycms_ie_form form", function(e) {

        var form = $(e.currentTarget);
        var obj = pycms.ie.formAsDict($(e.currentTarget));
        var model = $(e.currentTarget).data("model");

        if (form.data("object_id")) {
          obj.id = form.data("object_id");
          pycms.ie.updateObject(model, obj);

          var snippet = pycms.ie.renderTemplate(model, "view", obj);

          pycms.ie.updateContainers(model, snippet, obj.id);
          
          $(document).triggerHandler("pycms_ie_update_object", [model, obj]);
        } else {
          pycms.ie.addObject(model, obj);

          var snippet = pycms.ie.renderTemplate(model, "view", obj);

          pycms.ie.updateContainers(model, snippet);

          $(document).triggerHandler("pycms_ie_add_object", [model, obj]);
        }

        $("#pycms_ie_form").hide();
        $("#pycms_ie_form").html("");

        return false;
      });

    $(document).on("click", "#pycms_ie_form [type='button']", function(e) {
        $("#pycms_ie_form").hide();
        $("#pycms_ie_form").html("");
      });

    $(document).on("click", ".pycms_ie_editable", function(e) {

        var rec = $(e.currentTarget);

        rec.siblings().removeClass("selected");
        rec.toggleClass("selected");

        $(document).triggerHandler(
                                   "pycms_ie_select_object", 
                                   [rec.data("model"), 
                                    rec.data("object_id"),
                                    rec.hasClass("selected")]);
      });

    $(document).triggerHandler("pycms_ie_ready"); 


    $(document).on("submit", ".modal form", function(e) {

        var form = $(e.currentTarget);
        var modal = form.parents(".modal");

        $.post(form.attr("action"), 
               form.serialize(),
               function(data, status, xhr) {

                 if (xhr.status == 200) {
                   pycms.alert("ok", "success");
                   modal.hide();
                 } else if (xhr.status >= 300 && xhr.status < 400) {
                   pycms.alert("Something went wrong...", "error");
                   modal.hide();
                 } else {
                   modal.find(".modal-body").html(data);
                 }

               })

          return false;
      });
  });
