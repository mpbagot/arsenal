var resourceAdder = document.getElementById('resource_adder');
resourceAdder.parentNode.removeChild(resourceAdder);
var adderButton = document.getElementById('add_resource');
var isThumbImage = false;

function addResource(save_link) {
  var resources = document.getElementById('ext_resources');
  if (!save_link) {
    resourceAdder = resources.appendChild(resourceAdder);
    adderButton.parentNode.removeChild(adderButton);
  } else {
    //Create a new resource div
    var resource = document.createElement('DIV');
    resource.classList.add('resource');
    // Add the removal button
    var destroy = document.createElement('BUTTON');
    destroy.onclick = function() {
      this.parentNode.parentNode.removeChild(this.parentNode);
      sendResourceUpdate(false, '', '', this.parentNode);
    }
    destroy.innerHTML = 'X'
    destroy.type = "button";
    destroy.classList.add('remove_button');
    resource.appendChild(destroy);
    // Grab all of the details
    var link = document.getElementById('resource_link').value;
    var title = document.getElementById('resource_title').value;
    var text = document.createElement('P');
    text.innerHTML = ('Title: '+title);
    text.style.margin = '2px 20px';
    text.style.display = 'inline-block';
    resource.appendChild(text);
    var text = document.createElement('P');
    text.innerHTML = ('Link: '+link);
    text.style.margin = '2px 40px';
    resource.appendChild(text);
    // Reset the fields
    document.getElementById('resource_title').value = '';
    document.getElementById('resource_link').value = '';

    resources.appendChild(resource);
    adderButton = resources.appendChild(adderButton);
    resourceAdder.parentNode.removeChild(resourceAdder);

    sendResourceUpdate(true, title, link, resource);
  }
}
function sendResourceUpdate(toAdd, title, link, parent) {
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/tutorial/editor/', true);
  xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  if (toAdd) {
    xhr.onload = function() {
      if (xhr.status == 200) {
        parent.id = xhr.responseText;
      }
    }
    xhr.send('type=resource&action=add&title='+title+"&link="+link);
  } else {
    res_id = parent.id;
    xhr.send('type=resource&action=delete&resid='+res_id);
  }
}
function processText() {
  var text_area = document.getElementById('text_area');
  var required = document.getElementById('tutorial_content');
  var text = '[';
  for (i = 0; i < required.children.length; i++) {
    var child = required.children[i];
    // console.log(child.tagName);
    if (i != 0 && child.tagName.toLowerCase() == 'span') {
      var wrap = document.createElement('div');
      wrap.appendChild(child.children[1].cloneNode(true));
    } else if (i == 0) {
      var wrap = child.children[0];
    } else {
      continue;
    }
    text += '"'+wrap.innerHTML.replace(/\"/g, '\\"')+'",';
  }
  text = text.substring(0, text.length-1)+']';
  text_area.value = text;
  console.log(text);
}

function drag(ev) {
  var element = ev.target.innerHTML;
  var element_html = '';
  switch (element) {
    case 'Heading':
      element_html = '<h3 class="tutorial_h3" ondblclick="getHeading(this);">Double Click to Change Text</h3>';
      break;
    case 'Paragraph':
      element_html = '<p class="tutorial_p" ondblclick="grabParagraph(event, this);">Double Click to Change Text</p>';
      break;
    case 'Image':
      element_html = '<img class="tutorial_img">';
      break;
    case 'Blank Spacer':
      element_html = '<br class="tutorial_br">';
      break;
    case 'Spacer Line':
      element_html = '<hr class="tutorial_hr">';
      break;
    case 'Video':
      element_html = '<video class="tutorial_video" controls width="80%">Video is not supported</video>';
      break;
    case 'Thumbnail Image':
      element_html = '<img class="tutorial_thumb">'
      break;
    default:
      return;
  }
  var html = '<button onclick="this.parentNode.parentNode.removeChild(this.parentNode);" class="remove_button">X</button>'+element_html;
  ev.dataTransfer.setData("text", html);
  document.getElementById('dropper_info').innerHTML = "Drop Element here.";
}
function drop(ev) {
  ev.preventDefault();
  var files = ev.dataTransfer.files;
  if (files.length > 0) {
    if (files.length > 1) {
      return;
    }
    // upload the file and automatically embed it into the tutorial
    var file = files[0];
    var formData = new FormData();
    var src = '';
    formData.append('upload_file', file, file.name);

    var xhr = new XMLHttpRequest();

    xhr.open('POST', '/tutorial/upload', true);

    xhr.onload = function() {
      console.log('done');
      if (xhr.status == 200) {
        src = xhr.responseText;
        if (file.type.startsWith('image')) {
          //is an image
          if (isThumbImage) {
              data = '<img class="tutorial_thumb" src="'+src+'">';
          } else {
            data = '<img class="tutorial_img" src="'+src+'">';
          }
          isThumbImage = false;
        } else if (file.type.startsWith('video')) {
          //is a video
          data = '<video class="tutorial_video" src="'+src+'" controls>Video is not supported</video>';
        }
        data = '<button onclick="this.parentNode.parentNode.removeChild(this.parentNode);" class="remove_button">X</button>'+data;
        var span = document.createElement('SPAN');
        span.innerHTML = data;
        document.getElementById('tutorial_content').appendChild(span);
        document.getElementById('dropper_info').innerHTML = 'Drop elements here from the list on the left to add them to the tutorial';

      } else {
        document.getElementById('dropper_info').innerHTML = 'Upload Failed.';
      }
    };

    xhr.send(formData);

    document.getElementById('dropper_info').innerHTML = 'Uploading. Please wait.';
    return;

  } else {
    var data = ev.dataTransfer.getData("text");
    var dummy = document.createElement('DIV');
    dummy.innerHTML = data;
    var tag = dummy.children[1].tagName.toLowerCase();
    if (tag == 'video' || tag == "img") {
      document.getElementById('dropper_info').innerHTML = 'Please drag '+tag+' file here to upload.';
      if (dummy.children[1].className == 'tutorial_thumb') {
        isThumbImage = true;
      }
      return;
    }
  }
  var span = document.createElement('SPAN');
  span.innerHTML = data;
  document.getElementById('tutorial_content').appendChild(span);
  document.getElementById('dropper_info').innerHTML = 'Drop elements here from the list on the left to add them to the tutorial';
}
function grabParagraph(ev, paragraph) {
  var text_area = document.createElement('TEXTAREA');
  text_area.value = paragraph.innerHTML;
  text_area.id = 'current_paragraph';
  if (paragraph.children.length == 0) {
    paragraph.innerHTML = '';
    paragraph.appendChild(text_area);
  }
  document.onclick = function(e) {
    if (e == undefined) e = window.event;
    var targ = 'target' in e? e.target : e.srcElement;

    if (targ.id != 'current_paragraph') {
      var textarea = document.getElementById('current_paragraph');
      paragraph.innerHTML = textarea.value;
      textarea.parentNode.removeChild(textarea);
      document.onclick = null;
    }
  }
}
function getHeading(heading) {
  heading.innerHTML = prompt('Set Heading Text:', '');
  if (heading.innerHTML == null || heading.innerHTML == ''){
    heading.innerHTML = 'Heading';
  }
}
