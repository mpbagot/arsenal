var dropped = true;
var mustWait = false;
function toggleMenu() {
  if (!mustWait) {
    dropped = !dropped;
    mustWait = true;
    drop_menu = document.getElementById('drop_menu');
    if (dropped) {
      drop_menu.style.visibility = "visible";
      drop_menu.className = 'slideInMenuUp';
      setTimeout(function() {
        drop_menu.style.width = '20%';
        drop_menu.className = 'slideInMenuSide';
        setTimeout(function() {
          drop_menu.className = '';
          drop_menu.style.height = '200px';
          for (i in drop_menu.children) {
            var child = drop_menu.children[i];
            if (child.classList) {
              child.classList.remove('invisible');
            }
          }
          mustWait = false;
        }, 200);
      }, 300);
    } else {
      drop_menu.className = 'slideOutMenuSide';
      for (i in drop_menu.children) {
        var child = drop_menu.children[i];
        if (child.classList) {
          child.classList.add('invisible');
        }
      }
      setTimeout(function() {
        drop_menu.style.height = '0';
        drop_menu.className = 'slideOutMenuUp';
        setTimeout(function() {
          drop_menu.className = '';
          drop_menu.style.width = '0';
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
    button = document.getElementById('loginbutton');
    if (droppedUser) {
      menu.className = 'slideInUserMenu';
      button.style.visibility = 'visible';
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
          button.style.visibility = 'hidden';
          mustWaitUser = false;
        }, 400);
        setTimeout(function() {
          form.style.opacity = '0';
          form.className = '';
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
setTimeout(adjustDropMenu, 500);
adjustDropMenu(null);
