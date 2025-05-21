// Agregar al carrito
function agregarAlCarrito(id) {
  const producto = productos.find(p => p.id === id);
  if (!producto) return;

  const color = document.getElementById('color-seleccionado')?.value;
  const talla = document.getElementById('talla-seleccionada')?.value;
  const cantidad = parseInt(document.getElementById('cantidad-seleccionada')?.value) || 1;

  const carrito = JSON.parse(localStorage.getItem('carrito')) || [];

  carrito.push({
    id: producto.id,
    nombre: producto.nombre,
    imagen: producto.imagen,
    precio: Math.min(...producto.proveedores.map(p => p.precio)),
    color,
    talla,
    cantidad
  });

  localStorage.setItem('carrito', JSON.stringify(carrito));

  actualizarContadorCarrito();
  mostrarModalCarrito();
}

// Modal después de agregar
function mostrarModalCarrito() {
  const modal = document.getElementById("modal-carrito");
  if (modal) {
    modal.style.display = "flex";

    document.getElementById("seguir-viendo").onclick = function () {
      modal.style.display = "none";
    };

    document.getElementById("ir-carrito").onclick = function () {
      window.location.href = "carrito.html";
    };
  }
}

// Contador del carrito
function actualizarContadorCarrito() {
  const spanContador = document.getElementById('contador-carrito');
  if (!spanContador) return;

  const carrito = JSON.parse(localStorage.getItem('carrito')) || [];
  spanContador.textContent = carrito.length;
}

document.addEventListener("DOMContentLoaded", actualizarContadorCarrito);
