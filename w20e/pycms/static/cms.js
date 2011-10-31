var pycms = {};


var currGroup;
var currBlock;
var pasteBoard;
var do_edit = false;


pycms.showSubmenu = function(subId) {
  $("#" + subId).show();

  setTimeout('$("#' + subId + '").hide()', 5000);
}


function cutBlock() {

  if (currBlock && !currGroup.hasClass("fixed")) {
    pasteBoard = currBlock.remove();
    currBlock = false;
  }
}


function pasteBlock() {

  if (pasteBoard) {
    currGroup.append(pasteBoard);
    currBlock = pasteBoard;
    
    addEvents();
  }
}


/**
 * Delete the current block, unless it's fixed.
 */
function deleteBlock() {

  if (currBlock && !currBlock.hasClass("fixed")) {
    currBlock.remove();
    currBlock = false;
  } else {
    showMessage("You can't delete the main container");
  }
}


/**
 * Save the entire content block.
 */
function savePage() {

  var content = $("#content").html();

  $.post("save_page", {'content': content}, function(data, status) {
      if (status == 'error') {
        showMessage("Tough luck");
      } else {
        showMessage("Saved");
      }
    });
}


/**
 * Save the created block. This involves creating the html snippet on the
 * server, and adding it to the current document.
 */
function saveBlock(data) {

  if (data['type'] == 'image') {

    $("#img_save").load(function() {
        
        html = $("#img_save").contents().find("body").html();

        if (do_edit) {
          currBlock.replaceWith(html);
        } else {
          currGroup.append(html);
        }
        
        addEvents();
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
        
        addEvents();
      });

    return false;
  }
}


function editBlock() {

  do_edit = true;

  var data = getConfig(currBlock);  

  $("#form_target").load("edit_form", data, function() {

      if (status == 'error') {
        showMessage("Error in loading add form");
        return;
      }

      initForm();
      $("#mask").show('slow');
      $("#form_target").show('slow');
    });
}


function addBlock(type) {

  do_edit = false;

  $("#form_target").load("add_form", {'type': type}, function(txt, status) {

      if (status == 'error') {
        showMessage("Error in loading add form");
        return;
      }

      initForm();
      $("#mask").show('slow');
      $("#form_target").show('slow');
    });
}


addGroup = addBlock;


function createConfig(data) {

  html = '<dl class="config">'

  for (var key in data) {
    html += '<dt>' + key + '</dt><dd>' + data[key] + '</dd>';
  }

  html += '</dl>';

  return html;
}


function getConfig(tgt) {

  var cfg = {};
  
  tgt.children("dl").eq(0).children("dt").each(function() {
      cfg[$(this).html()] = $(this).next().html();
    });
  
  return cfg;
}


function createDataArray(form) {

  var dataArray = form.serializeArray();
  var data = {};
  
  for (var i = 0; i < dataArray.length; i++) {
    data[dataArray[i]['name']] = dataArray[i]['value'];
  }

  return data;
}


function initForm() {

  $('#form_target textarea.wysiwyg').tinymce({
        script_url : '/static/tinymce/jscripts/tiny_mce/tiny_mce.js',

        // General options
        theme : "advanced",
        plugins : "autolink,lists,pagebreak,style,layer,table,save,advhr,       advimage,advlink,inlinepopups,insertdatetime,preview,media,searchreplace,print, contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template,advlist",

        // Theme options
        theme_advanced_buttons1 : "bold,italic,underline,strikethrough,|,       justifyleft,justifycenter,justifyright,justifyfull,styleselect,|,cut,copy,paste,pastetext,pasteword,bullist,numlist,|,outdent,indent,blockquote,|,nonbreaking,  pagebreak,|,undo,redo",
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
      
      var data = createDataArray($("#form_target form"));
      var bubbleUp = false;
      
      try {
        bubbleUp = saveBlock(data);
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
function resized(event, ui) {

  $(this).find("dt:contains('width')").eq(0).next().html(ui.size.width + "px");
  $(this).find("dt:contains('height')").eq(0).next().html(ui.size.height + "px");
}


function dropped(event, ui) {

  $(this).find("dt:contains('top')").eq(0).next().html(ui.position.top + "px");
  $(this).find("dt:contains('left')").eq(0).next().html(ui.position.left + "px");
}


function showMessage(msg) {

  $("#msg").html(msg);  
  $("#msg").dialog();
}


/**
 * Bind event handlers to events.
 */
function addEvents() {

  $(".block").click(function(e) {

      $(".selected").toggleClass("selected");
      $(this).toggleClass("selected");

      if ($(this).hasClass("selected")) {
          currBlock = $(this);
        }
      //e.stopPropagation();
    });

  // resize and drag 'n drop...
  $(".block").resizable({grid: [5, 5], stop: resized}).draggable({
      'grid': [10, 10], 'stop': dropped});
}


/* db pack */
pycms.pack = function() {

  $.post("ajax_pack",          
         function(data) {
           $("#pack_result").html(data);
         });
}


/* Initialization sequence started... */
$(document).ready(function() {

    currGroup = $("#content");

    addEvents();

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
          theme_advanced_buttons1 : "bold,italic,underline,strikethrough,|,       justifyleft,justifycenter,justifyright,justifyfull,styleselect,|,cut,copy,paste,pastetext,pasteword,bullist,numlist,|,outdent,indent,blockquote,|,nonbreaking,  pagebreak,|,undo,redo",
          theme_advanced_buttons2 : "link,unlink,anchor,image,cleanup,code,|,     preview,|,forecolor,backcolor,tablecontrols,|,hr,removeformat,|,charmap,media,|,fullscreen",
          theme_advanced_buttons3 : "",
          theme_advanced_toolbar_location : "top",
          theme_advanced_toolbar_align : "left",
          theme_advanced_statusbar_location : "bottom",
          relative_urls : false,
          file_browser_callback:tinyupload
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
