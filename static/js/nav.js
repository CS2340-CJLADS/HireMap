function toggleUserMenu() {
  var menu = document.getElementById('userMenu');
  if (!menu) return;
  if (menu.style.display === 'none' || menu.style.display === '') {
    menu.style.display = 'block';
    document.addEventListener('click', outsideClickListener);
  } else {
    menu.style.display = 'none';
    document.removeEventListener('click', outsideClickListener);
  }
}

function outsideClickListener(e) {
  var menu = document.getElementById('userMenu');
  var button = document.querySelector('.avatar-btn');
  if (!menu || !button) return;
  var isClickInside = menu.contains(e.target) || button.contains(e.target);
  if (!isClickInside) {
    menu.style.display = 'none';
    document.removeEventListener('click', outsideClickListener);
  }
}


