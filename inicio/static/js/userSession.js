document.addEventListener("DOMContentLoaded", () => {
  const userArea = document.getElementById("user-area");
  const welcomeArea = document.getElementById("welcome-area");
  const welcomeMsg = document.getElementById("welcome-msg");
  const logoutBtn = document.getElementById("logout-btn");

  // Revisar si usuario está "logueado"
  function checkLogin() {
    const username = localStorage.getItem("username");
    if (username) {
      userArea.style.display = "none";
      welcomeMsg.textContent = `Hola, ${username}`;
      welcomeArea.style.display = "inline-block";
    } else {
      userArea.style.display = "inline-block";
      welcomeArea.style.display = "none";
    }
  }

  // Simular inicio sesión
  document.getElementById("login-link").addEventListener("click", (e) => {
    e.preventDefault();
    const nombre = prompt("Ingresa tu nombre para iniciar sesión:");
    if (nombre) {
      localStorage.setItem("username", nombre);
      checkLogin();
    }
  });

  // Cerrar sesión
  logoutBtn.addEventListener("click", () => {
    localStorage.removeItem("username");
    checkLogin();
  });

  checkLogin();
});