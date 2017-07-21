var resourceArray = {};

var resourceAdder = document.getElementById('resource_adder');
resourceAdder.parentNode.removeChild(resourceAdder);
var adderButton = document.getElementById('add_resource');

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
  xhr.open('POST', '/tutorial/editor', true);
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
