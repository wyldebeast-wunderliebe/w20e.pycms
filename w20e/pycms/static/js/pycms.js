var pycms = {};


var currGroup;
var currBlock;
var pasteBoard;
var do_edit = false;


pycms.alert = function(msg, type) {

  $("#alert").attr("class", "alert alert-" + type);
  $("#alert_msg").html(msg);
  $("#alert").show();
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

  $('#form_target textarea.wysiwyg').tinymce({
        script_url : '/static/js/tiny_mce/tiny_mce.js',

        // General options
        theme : "advanced",
        plugins : "autolink,lists,pagebreak,layer,table,save,advhr,       advimage,advlink,inlinepopups,insertdatetime,preview,media,searchreplace,print, contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template,advlist",

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


pycms.showMessage = function(msg) {

  $("#msg").html(msg);  
  $("#msg").dialog();

  setTimeout('$("#msg").parents(".ui-dialog").eq(0).fadeOut(300)', 3000);
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
  $(".block").resizable({grid: [5, 5], stop: pycms.resized}).draggable({
      'grid': [10, 10], 'stop': pycms.dropped});
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
}

/* Initialization sequence started... */
$(document).ready(function() {

    currGroup = $("#content");

    pycms.addEvents();

    $(".jsaction").click(function(e) {
        try {
          var f = eval($(this).attr("data-jscall"));
          f.call(e, e);
        } catch(e) {
          console.log(e);
        }

        return false;
      });

    // Enable dropdowns
    $('.dropdown-toggle').dropdown()

    $('textarea.wysiwyg').tinymce({
        script_url : '/static/tinymce/jscripts/tiny_mce/tiny_mce.js',

          // General options
          theme : "advanced",
          plugins : "autolink,lists,pagebreak,style,layer,table,save,advhr,       advimage,advlink,inlinepopups,insertdatetime,preview,media,searchreplace,print, contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template,advlist",
          
          // Theme options
          theme_advanced_buttons1 : "bold,italic,underline,strikethrough,|,       justifyleft,justifycenter,justifyright,justifyfull,formatselect,|,cut,copy,paste,pastetext,pasteword,bullist,numlist,|,outdent,indent,blockquote,|,nonbreaking,  pagebreak,|,undo,redo",
          theme_advanced_buttons2 : "link,unlink,anchor,image,cleanup,code,|,     preview,|,forecolor,backcolor,tablecontrols,|,hr,removeformat,|,charmap,media,|,fullscreen",
          theme_advanced_buttons3 : "",
          theme_advanced_toolbar_location : "top",
          theme_advanced_toolbar_align : "left",
          theme_advanced_statusbar_location : "bottom",
          relative_urls : false,
          file_browser_callback:tinyupload
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
});
