var isAdvancedUpload = function() {
  var div = document.createElement('div');
  return (('draggable' in div) || ('ondragstart' in div && 'ondrop' in div)) && 'FormData' in window && 'FileReader' in window;
}

var $form = $('.box');

if (isAdvancedUpload()) {
  $form.addClass('has-advanced-upload');

  var droppedFiles = false;

  $form.on('drag dragstart dragend dragover dragenter dragleave drop', function(e) {
    e.preventDefault();
    e.stopPropagation();
    $form.removeClass('is-error');
    $form.removeClass('is-success');
  })
  .on('dragover dragenter', function() {
    $form.addClass('is-dragover');
  })
  .on('dragleave dragend drop', function() {
    $form.removeClass('is-dragover');
  })
  .on('drop', function(e) {
    droppedFiles = e.originalEvent.dataTransfer.files;
    $form.trigger('submit');
  })
  .on('submit', function(e) {
    e.preventDefault();
    if ($form.hasClass('is-uploading')) return false;

    $form.addClass('is-uploading').removeClass('is-error');

    //AJAX upload for modern browsers
    var formData = new FormData();

    if (!droppedFiles) {
      droppedFiles = document.getElementById('svg_upload').files;
    }

    for (var i = 0; i < droppedFiles.length; i++) {
      var file = droppedFiles[i];
      if (file.name.substring(file.name.length-4, file.name.length) != '.svg') {
        $form.addClass('is-error');
        $form.removeClass('is-uploading');
        return;
      }
      formData.append('laser_img', file, file.name);
    }

    var xhr = new XMLHttpRequest();

    xhr.open('POST', '/upload', true);

    xhr.onload = function() {
      $form.removeClass('is-uploading');
      console.log('done');
      if (xhr.status == 200) {
        document.write(xhr.responseText);
        document.close();
        $form.addClass('is-success');
      } else {
        $form.addClass('is-error');
      }
    };

    xhr.send(formData);

  })
  .on('change', function(e) {
    $form.trigger('submit');
  });

  document.getElementById('box__button').style.display = 'none';
}
