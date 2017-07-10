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
          menu.className = '';
          menu.style.width = '0';
          mustWait = false;
        }, 300);
      }, 200);
    }
  }
}
var droppedUser = false;
var mustWaitUser = false;
function toggleUserMenu() {
  if (!mustWaitUser) {
    droppedUser = !droppedUser;
    mustWaitUser = true;
    menu = document.getElementById('slide_out');
    form = document.getElementById('user_menu');
    if (droppedUser) {
      menu.className = 'slideInUserMenu';
      setTimeout(function() {
        menu.style.marginLeft = '60%';
        menu.style.width = '40%';
        menu.className = '';
        setTimeout(function() {
          form.style.opacity = '1';
          form.className = '';
          mustWaitUser = false;
        }, 100);
      }, 400);
      setTimeout(function() {
        form.className = 'fadeIn';
      }, 300);
    } else {
      form.className = 'fadeOut';
      setTimeout(function() {
        menu.className = 'slideOutUserMenu';
        setTimeout(function() {
          menu.style.marginLeft = '75%';
          menu.style.width = '25%';
          menu.className = '';
        }, 400);
        setTimeout(function() {
          form.style.opacity = '0';
          form.className = '';
          mustWaitUser = false;
        }, 100);
      }, 100);
    }
  }
}

function adjustDropMenu(event) {
  height = document.getElementById('drop_button').height;
  document.getElementById('drop_menu').style.marginTop = '-'+(height+4)+'px';
  document.getElementById('drop_menu').style.paddingTop = (height+10)+'px';
}
window.onresize = adjustDropMenu;
setTimeout(adjustDropMenu, 1000);
// adjustDropMenu(null);
