// Abrir/cerrar menú principal en móvil
const menuToggleBtn = document.getElementById('menuToggleBtn');
const menuPrincipal = document.getElementById('menuPrincipal');

menuToggleBtn.addEventListener('click', () => {
  menuPrincipal.classList.toggle('active');
});

// Toggle submenus en móvil
const submenuToggles = document.querySelectorAll('.submenu-toggle');

submenuToggles.forEach(toggle => {
  toggle.addEventListener('click', (e) => {
    e.preventDefault();

    // Cerrar otros submenus
    submenuToggles.forEach(t => {
      if (t !== toggle) {
        t.parentElement.classList.remove('active');
      }
    });

    // Abrir/cerrar submenu actual
    toggle.parentElement.classList.toggle('active');
  });
});
