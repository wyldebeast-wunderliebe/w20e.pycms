var pycms = {};


var currGroup;
var currBlock;
var pasteBoard;
var do_edit = false;


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
        script_url : '/static/tinymce/jscripts/tiny_mce/tiny_mce.js',

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
}


pycms.showMessage = function(msg) {

  $("#msg").html(msg);  
  $("#msg").dialog();

  setTimeout('$("#msg").parents(".ui-dialog").eq(0).fadeOut(300)', 3000);
}


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


/* db pack */
pycms.pack = function() {

  $.post("ajax_pack",          
         function(data) {
           $("#pack_result").html(data);
         });
}

/* cut & paste of objects */
pycms.cut = function(item) {

    /*var cut_n_paste_buff = $.Storage.get("cut_n_paste");

    if (cut_n_paste_buff==undefined) {
	cut_n_paste_buff = Array();
    } else {
	cut_n_paste_buff = cut_n_paste_buff.split("::");
    }
    */

    var cut_n_paste_buff = new Array();

    cut_n_paste_buff.push(item.attr("id").substr(4));

    $.Storage.set("cut_n_paste", cut_n_paste_buff.join("::"));
}

pycms.paste = function() {
    $.Storage.get("cut_n_paste");

    if ($.Storage.get("cut_n_paste") == undefined) {
	return;
    }

    var data = {'objs': $.Storage.get("cut_n_paste")}

    $.post("ajax_move", data, function(data) {
	
	alert(data);

	$.Storage.set("cut_n_paste", "");
    });
}


/* Initialization sequence started... */
$(document).ready(function() {

    currGroup = $("#content");

    pycms.addEvents();

    $(".actionsubs").click(function() {
        $(this).hide();
      });

    $(".actionsubs").mouseleave(function() {
        $(this).hide();
      });

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
    });

    $(".lsdelete").click(function() {

        var to_remove = $(this);

        $("#rm_confirm").dialog({
            resizable: false,
              height:140,
              modal: true,
              buttons: {
              "Delete": function() {
                $( this ).dialog( "close" );

                var row = to_remove.parents("tr").eq(0);
        
                $.post("ajax_rm", 
                       {'content_id': to_remove.attr("id").substr(3)}, 
                       function() {
                         
                         row.remove();
                       });
              },
                "Cancel": function() {
                  $( this ).dialog( "close" );
                }
            }
          });
      });

    $(".listingcontent tbody").sortable({
        update: function(event, ui) {
            var order = $(this).sortable('toArray').toString();
            $.get('ajax_order', {order:order});
        }});
});
