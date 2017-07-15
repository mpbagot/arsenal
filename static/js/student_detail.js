var canvas = document.getElementById('progress_bar');
var ctx = canvas.getContext('2d');
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
