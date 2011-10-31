function tinyupload(field_name, url, type, win){

    /**
    The tiny upload callback hi-jacks the calling window and impliments an upload and visual 
    image selection.
    */
    win.resultIframeLoaded = false;

    win.tuSeclectedUrl = '';
    win.tuIframeLoaded = function(){}

    var wDoc = win.document;
    /*
    Build the UI.
    */
    var whiteOutDiv = wDoc.createElement('div');
    whiteOutDiv.setAttribute('id', 'tuWhiteOut');
    wDoc.body.appendChild(whiteOutDiv);
    whiteOutDiv.style.cssText = 'position:absolute;top:0px;left:0px;width:100%;height:100%;background:#F0F0EE;';
    var el1 = wDoc.createElement('div');
    el1.setAttribute('id', 'tuUiDiv');
    el1.style.cssText = 'color:#000;padding:20px;';
    whiteOutDiv.appendChild(el1);
    var uiDiv = wDoc.getElementById('tuUiDiv');
    //First fieldset.
    el1 = wDoc.createElement('fieldset');
    el1.style.cssText = 'background:#fff;padding:10px;';
    el1.setAttribute('id', 'tuFsUpload');
    uiDiv.appendChild(el1);
    var fs = wDoc.getElementById('tuFsUpload');
    el1 = wDoc.createElement('legend');
    el1.appendChild(wDoc.createTextNode('Upload'));
    fs.appendChild(el1);
    el1 = wDoc.createElement('div');
    el1.style.cssText = 'overflow:hidden;padding-bottom:5px;';
    el1.setAttribute('id', 'tuDivUpload');
    var el2 = wDoc.createElement('label');
    el2.appendChild(wDoc.createTextNode('Image Upload'));
    el2.style.cssText = 'width:120px;float:left;display:block;';
    el1.appendChild(el2);

    //upload form

    var uploadForm = $('<form class="tiny-upload-form" action=""><input id="tiny-upload-image" type="file" name="tiny-upload-image"/><input type="submit" id="formsubmit" name="upload" value="upload"/></form>');
    var resultIframe = $('<iframe id="upload_target" name="upload_target" src="#" style="width:0;height:0;border:0px solid #fff;"></iframe>');
    $(resultIframe).hide();

    $(el1).append(uploadForm);
    $(el1).append(resultIframe);

    $(uploadForm).find("#formsubmit").click(function() {
        var userFile = $(uploadForm).find('#tiny-upload-image').val();
        $(uploadForm).attr( "action", "/tiny_upload_image" )
        $(uploadForm).attr( "method", "post" )
        $(uploadForm).attr( "userfile", userFile )
        $(uploadForm).attr( "enctype", "multipart/form-data" )
        $(uploadForm).attr( "encoding", "multipart/form-data" )
        $(uploadForm).attr( "target", "upload_target" )
        $(uploadForm).submit();

        //need to get contents of the iframe
        if (win.resultIframeLoaded == false) {
            $(resultIframe).bind('load', function(){
                var iframeContents = $(resultIframe).contents().find('body').html();
                // we expect something like this:
                // <pre>{'status': 0, 'message': 'ok'}</pre>
                result = eval("response = " + $(iframeContents).html());
                if (result['status'] == 0) {
                    alert('Image uploaded');
                    load_images();
                } else {
                    alert('Failed to upload image: ' + result['message']);
                }
            });
            win.resultIframeLoaded = true;
        }
        return false;
    });

    fs.appendChild(el1);


    //Second fieldset.
    el1 = wDoc.createElement('fieldset');
    el1.setAttribute('id', 'tuFsSelect');
    el1.style.cssText = 'background:#fff;padding:10px;';
    uiDiv.appendChild(el1);
    fs = wDoc.getElementById('tuFsSelect');
    el1 = wDoc.createElement('legend');
    el1.appendChild(wDoc.createTextNode('Select'));
    fs.appendChild(el1);
    el1 = wDoc.createElement('div');
    el1.style.cssText = 'height:220px;border:1px solid #808080;overflow:auto;';
    el1.setAttribute('id', 'tuDivSelect');
    fs.appendChild(el1);
    //Buttons
    el1 = wDoc.createElement('input');
    el1.setAttribute('type', 'button');
    el1.setAttribute('value', 'Select');
    el1.style.cssText = 'float:left;width:100px;margin-top:5px;';
    el1.setAttribute('id', 'tuBtnSelect');
    uiDiv.appendChild(el1);
    el1 = wDoc.createElement('input');
    el1.setAttribute('type', 'button');
    el1.setAttribute('value', 'Cancel');
    el1.style.cssText = 'float:right;width:100px;margin-top:5px;';
    el1.setAttribute('id', 'tuBtnCancel');
    uiDiv.appendChild(el1);

    
    /*
    Events.
    */
    //Select
    function selectEvt(win){
        return function(){
            win.document.forms[0].elements[field_name].value = win.tuSeclectedUrl;
            win.document.forms[0].elements[field_name].onchange();
            win.document.body.removeChild(win.document.getElementById('tuWhiteOut'));
        }
    }
    wDoc.getElementById('tuBtnSelect').onclick = selectEvt(win);
    
    //Cancel
    function cancelEvt(win){
        return function(){
            win.document.body.removeChild(win.document.getElementById('tuWhiteOut'));
        }
    }
    wDoc.getElementById('tuBtnCancel').onclick = cancelEvt(win);
    
    win.tuFileUploadStarted = function(pth, nme){
        function rntUrl(pth){
            return function(){
                win.document.forms[0].elements[field_name].value = pth;
                win.document.forms[0].elements[field_name].onchange();
                win.document.body.removeChild(win.document.getElementById('tuWhiteOut'));
            }
        }
        win.tuIframeLoaded = rntUrl(pth);
        return true;
    }
    
    /*
    Ajax request 
    */

    function ajax_success(data) {
        function setUrl(u){
            return function(){
                win.tuSeclectedUrl = u;
                for (var j=0; j<win.tuImageList.length; j++){
                    if (win.tuSeclectedUrl == win.tuImageList[j].url){
                        wDoc.getElementById('tuSelectEl'+j).style.cssText = 'width:115px;height:128px;float:left;border:1px solid #83A57A;background-color:#CBFFBC;margin:1px;text-align:center;';
                    }
                    else{
                        wDoc.getElementById('tuSelectEl'+j).style.cssText = 'width:115px;height:128px;float:left;border:1px solid #fff;background-color:#fff;margin:1px;text-align:center;cursor:pointer;';
                    }
                }
            }
        }
    
        win.tuImageList = eval(data); 
        var imgList = win.tuImageList;

        // clear the list of images (in case of reload after upload)
        $(wDoc.getElementById('tuDivSelect')).empty();
        
        for (var i=0; i<imgList.length; i++){
            cont = wDoc.createElement('div');
            cont.setAttribute('id', 'tuSelectEl'+i);
            cont.style.cssText = 'width:115px;height:128px;float:left;border:1px solid #fff;background-color:#fff;margin:1px;text-align:center;cursor:pointer;';
            img = wDoc.createElement('img');
            img.setAttribute('src', imgList[i].thumb_url);
            img.style.cssText = 'width:110px;max-height:98px;border:1px solid #2020D2;';
            cont.appendChild(img);
            txt = wDoc.createElement('div');
            txt.appendChild(wDoc.createTextNode(imgList[i].file));
            cont.appendChild(txt);
            wDoc.getElementById('tuDivSelect').appendChild(cont);
            wDoc.getElementById('tuSelectEl'+i).onclick = setUrl(imgList[i].url);
            if (url == imgList[i].url){
                wDoc.getElementById('tuSelectEl'+i).style.cssText = 'width:115px;height:128px;float:left;border:1px solid #83A57A;background-color:#CBFFBC;margin:1px;text-align:center;';
            }
        }
    }

    function load_images() {
        $.ajax({
            url: "/tiny_browse_images",
            context: document.body,
            success: function(data){
                ajax_success(data);
            }
        });
    }

    load_images();

}
