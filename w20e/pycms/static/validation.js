/**
 * PyCMS validation.
 */
var w20e = {};
w20e.pycms = function() {};
w20e.pycms.VALIDATORS = [];


/**
 * Validation event handling.
 */
w20e.pycms.Validation = function(validation_url, options) {

  this.VALIDATION_URL = validation_url;
  this.form;
  this.lock;

  // Set defaults
  var defaults = {
    filter: false
  };  

  this.options = $.extend(defaults, options);
};


// Create Validation bindings. These result in interactive binding
// of validation to controls, Ajax style.
w20e.pycms.Validation.prototype.init = function(form) {
  
  var that = this;

  that.form = form;
  that.lock = false;

  form.find('.control :text').change(
                                     function() {
                                       that.validate($(this).serialize(), 
                                                     $(this));
                                     });
  
  form.find('.control select').change(
                                      function() {
                                        that.validate($(this).serialize(),
                                                      $(this));
                                      });
  
  form.find('.control textarea').change(
                                        function() {
                                          that.validate($(this).serialize(),
                                                        $(this));
                                        });
  
  form.find('.control :radio').click(
                                     function() {
                                       that.validate($(this).serialize(),
                                                     $(this));
                                     });
  
  form.find('.control :checkbox').click(
                                        function() {
                                          var name = $(this).attr("name");
                                          var data = {};
                                          data[name] = "";
                                          
                                          $(this).parents(".control").eq(0).find(":checkbox[name=" + name + "]:checked").each(function() {
                                              data[name] = data[name] + $(this).val() + ",";
                                            });
                                          
                                          that.validate(data, $(this));
                                        });
};



/**
 * Call server side validation.
 */
w20e.pycms.Validation.prototype.validate = function(data, caller) {

  var that = this;

  if (caller && that.options['filter']) {

    if (!that.options['filter'][caller.attr("name")]) {
      return;
    }
  }

  if (!data) {
    data = that.form.serialize();
  }

  // Are we already validating?
  if (that.lock) {
    return;
  }

  that.lock = true;

  $.post(that.VALIDATION_URL,
         data,
         function(doc) {
    
           //var doc = ( new DOMParser() ).parseFromString(data);
           var commands = doc.getElementsByTagName("command");
           
           for (var i = 0; i < commands.length; i++) {
             
             var selector = commands[i].getAttribute("selector");
             var command = commands[i].getAttribute("name");
             var value = commands[i].getAttribute("value");

             if (command == "alert") {
               $(selector).find(".alert").html(value);

               if (value != "") {
                 $(selector).addClass("err");
               } else {
                 $(selector).removeClass("err");
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

           // Finally, make sure card groups tabs are also checked...
           $(".cards li").each(function() {             

             var tab = $("div#" + $(this).attr('id').substr(4)).eq(0);

             if (tab.hasClass("readonly")) {
               $(this).addClass("readonly");
             } else {
               $(this).removeClass("readonly");
             }

             if (tab.hasClass("relevant")) {
               $(this).addClass("relevant");
             } else {
               $(this).removeClass("relevant");
             }

           });
           that.lock = false;
         },
         "xml");
};
