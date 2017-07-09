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
        }, 100);
      }, 400);
      setTimeout(function() {
        form.className = 'fadeIn';
      }, 300);
      mustWaitUser = false;
    } else {
      form.className = 'fadeOut';
      setTimeout(function() {
        menu.className = 'slideOutUserMenu';
        setTimeout(function() {
          menu.style.marginLeft = '82%';
          menu.style.width = '18%';
          menu.className = '';
        }, 400);
        setTimeout(function() {
          form.style.opacity = '0';
          form.className = '';
        }, 100);
      }, 100);
      mustWaitUser = false;
    }
  }
}
