// Mostrar el modal después de agregar al carrito
function mostrarModalCarrito() {
  const modal = document.getElementById("modal-carrito");
  if (modal) {
    modal.style.display = "flex";
    const btnSeguir = document.getElementById("seguir-navegando") || document.getElementById("seguir-viendo");
    if (btnSeguir) {
      btnSeguir.onclick = function () {
        modal.style.display = "none";
      };
    }
    const btnIrCarrito = document.getElementById("ir-carrito");
    if (btnIrCarrito) {
      btnIrCarrito.onclick = function () {
        window.location.href = "/cart/";
      };
    }
  }
}
window.mostrarModalCarrito = mostrarModalCarrito;

// Contador global
function actualizarContadorCarrito() {
  const spanContador = document.getElementById('contador-carrito');
  if (!spanContador) return;
  const carrito = JSON.parse(localStorage.getItem('carrito')) || [];
  // Suma todas las cantidades de productos
  const total = carrito.reduce((sum, p) => sum + (p.cantidad || 1), 0);
  spanContador.textContent = total;
}
document.addEventListener("DOMContentLoaded", actualizarContadorCarrito);
window.actualizarContadorCarrito = actualizarContadorCarrito;

// Agregar al carrito (puedes llamar esta función desde el botón en detalle)
function agregarAlCarrito(producto) {
  const carrito = JSON.parse(localStorage.getItem('carrito')) || [];
  const existente = carrito.find(p =>
    p.id == producto.id &&
    p.color == producto.color &&
    p.talla == producto.talla
  );
  if (existente) {
    existente.cantidad += producto.cantidad || 1;
  } else {
    carrito.push(producto);
  }
  localStorage.setItem('carrito', JSON.stringify(carrito));
  if (window.actualizarContadorCarrito) window.actualizarContadorCarrito();
}
window.agregarAlCarrito = agregarAlCarrito;

// Mostrar productos del carrito en la página de carrito
function mostrarCarrito() {
  const carrito = JSON.parse(localStorage.getItem('carrito')) || [];
  const listaCarrito = document.getElementById('productos-carrito');
  const totalCarrito = document.getElementById('total-carrito');
  if (!listaCarrito || !totalCarrito) return;

  // Limpiar la lista de productos
  listaCarrito.innerHTML = '';
  totalCarrito.innerHTML = '';

  if (carrito.length === 0) {
    listaCarrito.innerHTML = '<li>El carrito está vacío</li>';
  } else {
    let total = 0;
    carrito.forEach((producto, index) => {
      const li = document.createElement('li');
      li.innerHTML = `
        <img src="${producto.imagen}" alt="${producto.nombre}" style="width: 50px; height: 50px; margin-right: 10px;">
        <span>${producto.nombre}</span>
        <span>$${producto.precio}</span>
        <span>Cantidad: ${producto.cantidad}</span>
        <span>Color: ${producto.color}</span>
        <span>Talla: ${producto.talla}</span>
        <button onclick="eliminarDelCarrito(${index})">Eliminar</button>
      `;
      listaCarrito.appendChild(li);
      total += producto.precio * producto.cantidad;
    });
    totalCarrito.innerHTML = `<strong>Total a pagar: $${total.toFixed(0)}</strong>`;
  }
}

// Eliminar un producto del carrito
function eliminarDelCarrito(index) {
  const carrito = JSON.parse(localStorage.getItem('carrito')) || [];
  carrito.splice(index, 1);
  localStorage.setItem('carrito', JSON.stringify(carrito));
  mostrarCarrito();
  actualizarContadorCarrito();
}

// Vaciar el carrito
function vaciarCarrito() {
  localStorage.removeItem('carrito');
  mostrarCarrito();
  actualizarContadorCarrito();
}

// Inicializar funciones en la página de carrito
document.addEventListener("DOMContentLoaded", function() {
  mostrarCarrito();
  actualizarContadorCarrito();
});