if (pycms == undefined) {
  var pycms = {};
}


var currGroup;
var currBlock;
var pasteBoard;
var do_edit = false;


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


pycms.cutBlock = function() {

  if (currBlock && !currGroup.hasClass("fixed")) {
    pasteBoard = currBlock.remove();
    currBlock = false;
  }
}


pycms.pasteBlock = function() {

  if (pasteBoard) {
    currGroup.append(pasteBoard);
    currBlock = pasteBoard;

    pycms.addEvents();
  }
}


/**
 * Delete the current block, unless it's fixed.
 */
pycms.deleteBlock = function() {

  if (currBlock && !currBlock.hasClass("fixed")) {
    currBlock.remove();
    currBlock = false;
  } else {
    pycms.showMessage("You can't delete the main container");
  }
}


/**
 * Save the entire content block.
 */
pycms.savePage = function() {

  var content = $("#content").html();

  $.post("save_page", {'content': content}, function(data, status) {
      if (status == 'error') {
        pycms.showMessage("Tough luck");
      } else {
        pycms.showMessage("Saved");
      }
    });
}


/**
 * Save the created block. This involves creating the html snippet on the
 * server, and adding it to the current document.
 */
pycms.saveBlock = function(data) {

  if (data['type'] == 'image') {

      // Bind onload to img save iframe
      $("#img_save").load(function() {

      var html = $("#img_save").contents().find("html").html();

          if (do_edit) {
              currBlock.replaceWith(html);
          } else {
              currGroup.append(html);
          }

          pycms.addEvents();
      });

      // Let the original submit handle it from here...
      return true;

  } else {

      $.post("save_block", data, function(data) {

          if (do_edit) {
              currBlock.replaceWith(data);
          } else {
              currGroup.append(data);
          }

          pycms.addEvents();
      });

      return false;
  }
}


pycms.editBlock = function() {

  do_edit = true;

  var data = pycms.getConfig(currBlock);

  $("#form_target").load("edit_form", data, function() {

      if (status == 'error') {
        pycms.showMessage("Error in loading add form");
        return;
      }

      pycms.initForm();
      $("#mask").show('slow');
      $("#form_target").show('slow');
    });
}


pycms.addBlock = function(type) {

  do_edit = false;

  $("#form_target").load("add_form", {'type': type}, function(txt, status) {

      if (status == 'error') {
        pycms.showMessage("Error in loading add form");
        return;
      }

      pycms.initForm();
      $("#mask").show('slow');
      $("#form_target").show('slow');
    });
}


pycms.addGroup = pycms.addBlock;


pycms.selectLayout = function(type) {

}


pycms.createConfig = function(data) {

    html = '<dl class="config">'

    for (var key in data) {
      html += '<dt>' + key + '</dt><dd>' + data[key] + '</dd>';
    }

    html += '</dl>';

    return html;
}


pycms.getConfig = function(tgt) {

    var cfg = {};

    tgt.children("dl").eq(0).children("dt").each(function() {
      cfg[$(this).html()] = $(this).next().html();
    });

    return cfg;
}


pycms.createDataArray = function(form) {

    var dataArray = form.serializeArray();
    var data = {};

    for (var i = 0; i < dataArray.length; i++) {
      data[dataArray[i]['name']] = dataArray[i]['value'];
    }

    return data;
}


pycms.initForm = function() {

  var global_directionality = $('html').attr('dir') || 'ltr';

  $('#form_target textarea.wysiwyg').each(function() {

      var directionality = $(this).attr('dir') || global_directionality;

      $(this).tinymce({
        script_url : '/static/js/tiny_mce/tiny_mce.js',

        // General options
        directionality: directionality,
        theme : "advanced",
        plugins : "autolink,lists,pagebreak,layer,table,save,advhr,advimage,advlink,inlinepopups,insertdatetime,preview,media,searchreplace,print, contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template,advlist",

        // Theme options
        theme_advanced_buttons1 : "bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,headerselect,|,cut,copy,paste,pastetext,pasteword,bullist,numlist,|,outdent,indent,blockquote,|,nonbreaking,  pagebreak,|,undo,redo",
        theme_advanced_buttons2 : "link,unlink,anchor,image,cleanup,code,|,preview,|,forecolor,backcolor,tablecontrols,|,hr,removeformat,|,charmap,media,|,fullscreen",
        theme_advanced_buttons3 : "",
        theme_advanced_toolbar_location : "top",
        theme_advanced_toolbar_align : "left",
        theme_advanced_statusbar_location : "bottom",
        theme_advanced_resizing : true,
        relative_urls : false,
        file_browser_callback:tinyupload,
        onchange_callback : function(instance){
            $('#' + instance.editorId).trigger("change");
        }
    });
  });

  $("#form_target input[name=cancel]").click(function(e) {

      $("#form_target").html("");
      $("#mask").hide('slow');
      $("#form_target").hide('slow');
    });

  $("#form_target form").submit(function() {

      var data = pycms.createDataArray($("#form_target form"));
      data = $.extend({}, pycms.getConfig($("#" + data['id'])), data);

      var bubbleUp = false;

      try {
        bubbleUp = pycms.saveBlock(data);
      } catch (e) {
      }

      $("#form_target").hide('slow');
      $("#mask").hide('slow');

      return bubbleUp;
    });
}


/**
 * After-resize call that takes care of setting the size in the config.
 */
pycms.resized = function(event, ui) {

  $(this).find("dt:contains('width')").eq(0).next().html(ui.size.width + "px");
  $(this).find("dt:contains('height')").eq(0).next().html(ui.size.height + "px");
}


pycms.dropped = function(event, ui) {

  $(this).find("dt:contains('top')").eq(0).next().html(ui.position.top + "px");
  $(this).find("dt:contains('left')").eq(0).next().html(ui.position.left + "px");
};


pycms.showMessage = function(msg, title, as_html, timeout) {

  if (typeof title == "undefined") {
    title = "Incoming message";
  }

  if (typeof as_html == "undefined") {
      as_html = false;
  }

  if (typeof timeout == "undefined") {
      timeout = 2000;
  }

  $('#pycms-modal-label').text(title);

  if (as_html) {
      $('#pycms-modal .modal-body p').html(msg);
  } else {
      $('#pycms-modal .modal-body p').text(msg);
  }

  $('#pycms-modal').modal('show');

  if (timeout) {
      setTimeout(function(){$('#pycms-modal').modal('hide')}, timeout);
  }
};


pycms.about = function() {
  $("#about").show();
};

/**
 * Bind event handlers to events.
 */
pycms.addEvents = function() {

  $(".block").click(function(e) {

      $(".selected").toggleClass("selected");
      $(this).toggleClass("selected");

      if ($(this).hasClass("selected")) {
          currBlock = $(this);
        }
      //e.stopPropagation();
    });

  // resize and drag 'n drop...
  //$(".block").resizable({grid: [5, 5], stop: pycms.resized}).draggable({
  //    'grid': [10, 10], 'stop': pycms.dropped});
}


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
  var content_id = row.data("objectpath");
  var content_title = row.data("objecttitle");

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
  var content_id = row.data("objectpath");
  var content_title = row.data("objecttitle");

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

    $.Storage.set("paste_buffer", buffer);
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
}

pycms.bind_form_changes = function() {

    $(document).on("change", '.w20e-form.ajax-validate input[type="text"]', function(e) {
        $(e.target).closest("form.w20e-form").submit();
      });

    $(document).on("focusout", '.w20e-form.ajax-validate input[type="date"]', function(e) {
        $(e.target).closest("form.w20e-form").submit();
      });

    $(document).on("focusout", '.w20e-form.ajax-validate input[type="month"]', function(e) {
        $(e.target).closest("form.w20e-form").submit();
      });

    $(document).on("change", '.w20e-form.ajax-validate input[type="hidden"]', function(e) {
        $(e.target).closest("form.w20e-form").submit();
      });

    $(document).on("save", '.w20e-form.ajax-validate input[type="hidden"]', function(e) {
        $(e.target).closest("form.w20e-form").submit();
      });

    $(document).on("change", '.w20e-form.ajax-validate select', function(e) {
        $(e.target).closest("form.w20e-form").submit();
      });

    $(document).on("change", '.w20e-form.ajax-validate textarea', function(e) {
        $(e.target).closest("form.w20e-form").submit();
      });

    $(document).on("click", '.w20e-form.ajax-validate input[type="radio"]', function(e) {
        $(e.target).closest("form.w20e-form").submit();
      });
};

pycms.init_form_submission = function() {
  $(document).on("submit", 'form.w20e-form.ajax-validate', function(e) {
     var form = $(e.target);
     var errors = pycms.validate_form(form);
     return false; // prevent a non-ajax form submit
  });
};

pycms.validate_form = function(form) {

        var action = form.attr("action");
        var method = form.attr("method");
        var data = form.serialize();

        var errors = false;

        $.ajax({
            url: action,
              type: method,
              cache: false,
              data: data,
              success: function(doc) {

                var willRedirect = false;

                //var doc = ( new DOMParser() ).parseFromString(data);
                var commands = doc.getElementsByTagName("command");

                for (var i = 0; i < commands.length; i++) {

                    var selector = commands[i].getAttribute("selector");
                    var command = commands[i].getAttribute("name");
                    var value = commands[i].getAttribute("value");

                    if (command == "redirect") {
                        willRedirect = true;
                        window.location.replace(value);
                    }

                    if (command == "alert") {
                      $(selector).find(".alert").html(value);

                      if (value != "") {
                          $(selector).addClass("error");
                          errors = true;
                      } else {
                          $(selector).removeClass("error");
                      }
                    }

                    if (command == "calculate") {
                      /* find out the type of the selected control
                        for now only act on simple html elements, not on
                        other controls like selects, inputs etc
                      */
                        if ($(selector).hasClass('renderable')) {
                          $(selector).html(value);
                        }
                    }

                    if (value == "True") {
                      $(selector).addClass(command);

                      if (command == "readonly") {
                          $(selector + " :input").each(function() {
                              $(this).attr("disabled", "disabled");
                          });
                      }
                    } else {
                      $(selector).removeClass(command);

                      if (command == "readonly") {
                          $(selector + " :input").each(function() {
                              $(this).removeAttr("disabled");
                          });
                      }
                    }
                }


                // Finally, handle the card groups (tabs)
                form.find('.tab-pane').each(function() {
                    errors_in_tab = $(this).find('.error').length > 0;
                    var id = (this).id;
                    var tab_link = $("a[href='#" + id + "']");
                    if(errors_in_tab) {
                        tab_link.addClass('error');
                    } else {
                        tab_link.removeClass('error');
                    }

                });

                form.trigger("w20e_form_validated", [willRedirect]);

              },
              error: function() {
                alert("The form could not be processed. Changes will be lost!");
              }
          });

      return !errors;
};

pycms.escapeHTML = function(s) {
    return s.replace(/&(?!\w+;)/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

/* Initialization sequence started... */
$(document).ready(function() {

    currGroup = $("#content");

    pycms.addEvents();

    $(".jsaction").click(function(e) {
        try {
          var f = eval($(this).data("jscall"));
          f.call(e, e);
        } catch(e) {
          console.log(e);
        }

        return false;
      });

    var global_directionality = $('html').attr('dir') || 'ltr';


    $('textarea.wysiwyg').each(function() {

        var directionality = $(this).attr('dir') || global_directionality;

        $(this).tinymce({
          script_url : '/static/tinymce/jscripts/tiny_mce/tiny_mce.js',

          // General options
          directionality: directionality,
          theme : "advanced",
          plugins : "autolink,lists,pagebreak,style,layer,table,save,advhr,advimage,advlink,inlinepopups,insertdatetime,preview,media,searchreplace,print, contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template,advlist",

          // Theme options
          theme_advanced_buttons1 : "bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,formatselect,|,cut,copy,paste,pastetext,pasteword,bullist,numlist,|,outdent,indent,blockquote,|,nonbreaking,  pagebreak,|,undo,redo",
          theme_advanced_buttons2 : "link,unlink,anchor,image,cleanup,code,|,preview,|,forecolor,backcolor,tablecontrols,|,hr,removeformat,|,charmap,media,|,fullscreen",
          theme_advanced_buttons3 : "",
          theme_advanced_toolbar_location : "top",
          theme_advanced_toolbar_align : "left",
          theme_advanced_statusbar_location : "bottom",
          relative_urls : false,
          file_browser_callback:tinyupload,
          onchange_callback : function(instance){
              $('#' + instance.editorId).trigger("change");
          }
        });
    });

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

                   var tr = input.parents("tr");
                   tr.attr("id", id_to);
                   tr.data('objectid', id_to);

                   // replace last part of the dotted objectpath with the new id
                   var objectpath = tr.data('objectpath');
                   var newObjectpath = objectpath.replace(/(^.*\.).*$/, '$1' + id_to);
                   tr.data('objectpath', newObjectpath);

                   tr.find(".content-edit-link").attr('href', id_to + "/edit");
                   tr.find(".content-admin-link").attr('href', id_to + "/admin");
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
                     {'content_id': row.data("objectid")},
                     function() {
                       row.remove();
                     });
              $("#confirm_delete").modal('hide');
              return false;
            });

          $("#confirm_delete #object_title").html(row.data("objecttitle"));
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

    // enable bootstrap navigation (tabs). not sure if this should be done here
    $(".nav.nav-tabs.cards a").click(function (e) {
      e.preventDefault();
      $(this).tab('show');
    });

    pycms.bind_form_changes();
    pycms.init_form_submission();

    pycms.setAutofocus();

});


