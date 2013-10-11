var pycms = {};


var currGroup;
var currBlock;
var pasteBoard;
var do_edit = false;


pycms.TINYCONFIG = {
  script_url : '/static/3dparty/tinymce-4.0.2/js/tinymce/tinymce.min.js',

  // General options
  theme : "modern",
  plugins : "autolink,lists,pagebreak,layer,table,save,hr,image,link,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,template,advlist",

  // Theme options
  theme_advanced_buttons1 : "bold,italic,underline,strikethrough,|,       justifyleft,justifycenter,justifyright,justifyfull,headerselect,|,cut,copy,paste,pastetext,pasteword,bullist,numlist,|,outdent,indent,blockquote,|,nonbreaking,  pagebreak,|,undo,redo",
  theme_advanced_buttons2 : "link,unlink,anchor,image,cleanup,code,|,     preview,|,forecolor,backcolor,tablecontrols,|,hr,removeformat,|,charmap,media,|,fullscreen",
  theme_advanced_buttons3 : "",
  theme_advanced_toolbar_location : "top",
  theme_advanced_toolbar_align : "left",
  theme_advanced_statusbar_location : "bottom",
  theme_advanced_resizing : true,
  relative_urls : false,
  file_browser_callback:tinyupload
};


pycms.alert = function(msg, type) {

  $("#alert").attr("class", "alert alert-" + type);
  $("#alert_msg").html(msg);
  $("#alert").show();

  setTimeout("$('#alert').hide()", 3000);
}


pycms.showSubmenu = function(subId) {
  $("#" + subId).show();

  setTimeout('$("#' + subId + '").hide()', 5000);
}


pycms.createDataArray = function(form) {

    var dataArray = form.serializeArray();
    var data = {};

    for (var i = 0; i < dataArray.length; i++) {
      data[dataArray[i]['name']] = dataArray[i]['value'];
    }

    return data;
}


/**
 * Initialize widgets, i.e. TinyMCE and the likes
 */
pycms.init_widgets = function(tgt) {

  if (tgt) {
    tgt.find('textarea.wysiwyg').tinymce(pycms.TINYCONFIG);
  } else {
    $('textarea.wysiwyg').tinymce(pycms.TINYCONFIG);
  }
}


pycms.showMessage = function(msg, title) {

  if (typeof title == "undefined") {
    title = "Incoming message";
  }

  $('#pycms-modal-label').text(title);
  $('#pycms-modal .modal-body p').text(msg);

  $('#pycms-modal').modal('show');

  setTimeout(function(){$('#pycms-modal').modal('hide')}, 2000);
};


/**
 * Show 'about' popup
 */
pycms.about = function() {
  $("#about").show();
};


/**
 * Pack DB.
 * @param e Event containing the button that fired the event.
 */
pycms.pack = function(e) {

  if ($(e.target).hasClass("disabled")) {
    return;
  }

  $("body").css("cursor", "progress");
  $(e.target).addClass("disabled");

  $.ajax({'url': "ajax_pack",
        'type': "POST",
        'success': function(data) {
        $("#pack_result").html(data);
        $("body").css("cursor", "auto");
        $(e.target).removeClass("disabled");
      },
        'error': function(data) {
        $("#pack_result").html(data);
        $("body").css("cursor", "auto");
        $(e.target).removeClass("disabled");
      }});
}

/* cut & paste of objects */

/**
 * Cut item and push onto cut buffer.
 * @param item Item to cut.
 */
pycms.cut = function(item) {

  var row = item.parents("tr").eq(0);
  var content_id = row.attr("data-objectpath");
  var content_title = row.attr("data-objecttitle");

  var buffer = $.Storage.get("paste_buffer") || "";

  buffer += "::" + content_title + ";;" + content_id + ";;" + "cut";

  $.Storage.set("paste_buffer", buffer);

  pycms.alert("Paste buffer:<br/>" + buffer, "info");

  row.remove();
};


/**
 * Clear the cut buffer.
 */
pycms.clearCutBuffer = function() {
  $.Storage.set("paste_buffer", "");
  pycms.alert("Paste buffer cleared", "info");
}


/**
 * Copy item.
 */
pycms.copy = function(item) {

  var row = item.parents("tr").eq(0);
  var content_id = row.attr("data-objectpath");
  var content_title = row.attr("data-objecttitle");

  var buffer = $.Storage.get("paste_buffer") || "";

  buffer += "::" + content_title + ";;" + content_id + ";;" + "copy";

  $.Storage.set("paste_buffer", buffer);

  pycms.alert("Paste buffer:<br/>" + buffer, "info");
}


/**
 * Paste items.
 */
pycms.paste = function() {

    if ($.Storage.get("paste_buffer") == undefined) {
      return;
    }

    $.ajax({"url": "ajax_paste",
            "type": "POST",
            "data": {'buffer': $.Storage.get("paste_buffer")},
            "success": function(data) {
               pycms.alert(data, "success");
               $.Storage.set("paste_buffer", "");
        },
            "error": function(data) {pycms.alert(data, "error")}
      });
};


pycms.rename = function() {
    $("#rename").show();
};


/**
 * Add or remove nature.
 * @param event Click event that is attached to nature checkbox.
 */
pycms.nature = function(event) {

  var tgt = $(event.target);

  if (tgt.attr("checked")) {
    $.post("ajax_add_nature", {'nature_id': tgt.attr("name")},
           function(data) {
             tgt.attr("checked", "yes")
             pycms.alert("Added nature " + tgt.attr("name"), "success");
           });
  } else {
    $.post("ajax_remove_nature", {'nature_id': tgt.attr("name")},
           function(data) {
             pycms.alert("Removed nature " + tgt.attr("name"), "success");
             tgt.removeAttr("checked")
           });
  }
};


/**
 * read the variables from the 'extra-options' data attribute
 * and initialize the jquery datetimepicker
 */
pycms.enableDateTimePicker = function($element) {
    var extra_options =  $element.data('extra-options') || {};
    // do boolean conversion.. probably not the best place to do it
    if (extra_options.showTimepicker == 'false') {
        extra_options.showTimepicker = false;
    }
    if (!extra_options.dateFormat) {
        extra_options.dateFormat = 'yy-mm-dd';
    }
    $element.find('input').datetimepicker(extra_options);
}


/**
 * Set the focus to first active empty input field, with class autofocus
 */
pycms.setAutofocus = function() {
    var done = $(":input.autofocus[value='']:visible:enabled:first").focus();
    // if not found, try to find autofocus field which has a value
    if (done.length == 0) {
        done = $(":input.autofocus:visible:enabled:first").focus();
    }
    // if not found, try first w20e-form input which has an error
    if (done.length == 0) {
        done = $(".w20e-form .error :input:visible:enabled:first").focus();
    }
    // if not found, try first w20e-form input
    if (done.length == 0) {
        done = $(".w20e-form :input:visible:enabled:first").focus();
    }
};


/**
 * Initialize file uploading
 */
pycms.init_fileupload = function() {

  var defaults = {
    url: './upload_image',
    dataType: 'json',
    done: function (e, data) {
      
    },
    progress: function (e, data) {
      var progress = parseInt(data.loaded / data.total * 100, 10);
      $($(e.target).data("progress") + " .bar").css("width", progress + "%");
    }
  };
  
  $("#fileupload").each(function() {

      $(this).fileupload(defaults);
    });
};


/* Initialization sequence started... */
$(document).ready(function() {

    currGroup = $("#content");

    $(document).on("click", ".jsaction", function(e) {

        var link = $(e.currentTarget);

        $.post(link.attr("href"), link.data("params"), function(data) {
            
            pycms.alert(data['msg'], data['status']);
          }); 

        e.preventDefault();
      });

    $('textarea.wysiwyg').tinymce(pycms.TINYCONFIG);

    $(".lscut").click(function() {

        pycms.cut($(this));
        return false;
      });

    $(".lscopy").click(function() {

        pycms.copy($(this));
        return false;
      });

    // Handle rename function
    $(".rename").click(function() {
        $(this).find(".rename_in").show();
        $(this).find(".rename_in").focus();
      });

    // Losing focus here...
    $(".rename_in").blur(function() {
        $(this).val($(this).prev().text());
        $(this).hide();
      });

    $("#rename").submit(function() {

        $.post($(this).attr("action"), $(this).serialize(),
               function(data) {

                 for (id_from in data['renamed']) {

                   var id_to = data['renamed'][id_from];
                   var input = $("input[name='" + id_from + "']").eq(0);

                   input.attr("name", id_to);
                   input.attr("value", id_to);
                   input.prev().html(id_to);
                   input.hide();

                   input.parents("tr").eq(0).attr("id", id_to);
                 }
               });

        return false;
      })

      // Remove object and row
      //
      $(".lsdelete").click(function() {

          var row = $(this).parents("tr").eq(0);

          $("#confirm_delete .confirm").unbind('click');
          $("#confirm_delete .confirm").click(function() {
              $.post("ajax_rm",
                     {'content_id': row.attr("data-objectid")},
                     function() {
                       row.remove();
                     });
              $("#confirm_delete").modal('hide');
              return false;
            });

          $("#confirm_delete #object_title").html(row.attr("data-objecttitle"));
          $("#confirm_delete").modal();

          return false;
        });

    // Order objects on screen and on server
    //
    $(".contentlisting tbody").sortable({
        handle: '.contenttype',
        update: function(event, ui) {
          var order = $(this).sortable('toArray').toString();
          $.get('ajax_order', {order: order});
        }});

    $(".datetime").each(function(){
      pycms.enableDateTimePicker($(this));
    });

    pycms.setAutofocus();

    $("#pycms-modal").on("shown", function() {
        pycms.init_widgets($("#pycms-modal"));
      });

    $("#pycms-modal").on("hide", function() {
        $(this).removeData('modal');
        $(this).find(".modal-body").html("");
      });

    pycms.init_fileupload();

    // Handle explorer
    $(document).on("click", "#xplorer a", function(e) {

        $.get($(e.currentTarget).attr("href"),
              $(e.currentTarget).data("args"),
              function(data) {
                $("#xplorer").replaceWith(data);
              });

        e.stopPropagation();
        e.preventDefault();
      });
});
