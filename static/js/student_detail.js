var canvas = document.getElementById('progress_bar');
var ctx = canvas.getContext('2d');
function drawBar() {
  var text = 'Tutorials Completed: '+completed+'/'+100;
  var per = completed/100;
  document.getElementById('progress_heading').innerHTML = completed+"/100 Tutorials Completed";
  ctx.clearRect(0, 0, 400, 50);
  // Draw the loading bar
  ctx.fillStyle = '#FF905A';
  ctx.strokeStyle = '#FF7012';
  ctx.strokeRect(0, 0, 400, 50);
  ctx.fillRect(0, 0, 400*per, 50);
  // Set up the text styling
  ctx.fillStyle = 'black';
  ctx.font = 'normal 18pt Calibri';
  ctx.textAlign = 'center';
  // Draw the string
  ctx.fillText(text, canvas.width/2, 35);  // And display it on the canvas
}

function toggleComplete(tutorial_id, student_id) {
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/update/complete', true);
  xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  xhr.onload = function() {
    if (xhr.status == 200) {
      console.log('bleh');
      var box = document.getElementById('tutorial_'+tutorial_id);
      if (xhr.responseText == 'True') {
        box.classList.add('complete');
        completed += 1;
      } else {
        box.classList.remove('complete');
        completed -= 1;
      }
    }
  }
  xhr.send('studentid='+student_id+"&"+"tutid="+tutorial_id);
}
function toggleFlag(tutorial_id, student_id) {
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/update/flag', true);
  xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  xhr.onload = function() {
    if (xhr.status == 200) {
      var box = document.getElementById('tutorial_'+tutorial_id);
      if (xhr.responseText == 'True') {
        box.classList.add('flagged');
      } else {
        box.classList.remove('flagged');
      }
    }
  }
  xhr.send('studentid='+student_id+"&"+"tutid="+tutorial_id);
}
window.setInterval(drawBar, 200);
