var dropped = false;
var mustWait = false;
function toggleMenu() {
  if (!mustWait) {
    dropped = !dropped;
    mustWait = true;
    menu = document.getElementById('drop_menu');
    if (dropped) {
      menu.style.visibility = "visible";
      menu.className = 'slideInMenuUp';
      setTimeout(function() {
        menu.style.width = '20%';
        menu.className = 'slideInMenuSide';
        setTimeout(function() {
          menu.className = '';
          menu.style.height = '200px';
          mustWait = false;
        }, 200);
      }, 300);
    } else {
      menu.className = 'slideOutMenuSide';
      setTimeout(function() {
        menu.style.height = '0';
        menu.className = 'slideOutMenuUp';
        setTimeout(function() {
          // menu.style.visibility = 'hidden';
          menu.className = '';
          menu.style.width = '0';
          mustWait = false;
        }, 300);
      }, 200);
    }
  }
}
