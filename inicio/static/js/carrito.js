// Agregar al carrito
function agregarAlCarrito(id) {
  const producto = productos.find(p => p.id === id);
  if (!producto) return;

  // Selección de color y talla usando querySelector para obtener el valor del radio button seleccionado
  const color = document.querySelector('input[name="color"]:checked')?.value;
  const talla = document.querySelector('input[name="talla"]:checked')?.value;
  const cantidad = parseInt(document.getElementById('cantidad-seleccionada')?.value) || 1;

  if (!color || !talla) {
    alert('Por favor, selecciona color y talla antes de agregar al carrito');
    return; // No agregar al carrito si no hay color ni talla seleccionados
  }

  // Eliminamos los decimales y guardamos el precio como entero
  const precioSinDecimales = Math.floor(Math.min(...producto.proveedores.map(p => p.precio)));
    
  const carrito = JSON.parse(localStorage.getItem('carrito')) || [];

// Buscar si ya existe el mismo producto con mismo id, color y talla
const productoExistente = carrito.find(p =>
  p.id === producto.id &&
  p.color === color &&
  p.talla === talla
);

if (productoExistente) {
  // Si ya existe, solo sumamos la cantidad
  productoExistente.cantidad += cantidad;
} else {
  // Si no existe, lo agregamos como nuevo
  carrito.push({
    id: producto.id,
    nombre: producto.nombre,
    imagen: producto.imagen,
    precio: precioSinDecimales,
    color,
    talla,
    cantidad
  });
}

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


//Muestra lo que tiene el carro 
document.addEventListener("DOMContentLoaded", mostrarCarrito);

function mostrarCarrito() {
  const carrito = JSON.parse(localStorage.getItem('carrito')) || [];
  const listaCarrito = document.getElementById('productos-carrito');
  const totalCarrito = document.getElementById('total-carrito');
  
  // Limpiar la lista de productos
  listaCarrito.innerHTML = '';
  totalCarrito.innerHTML = '';

  if (carrito.length === 0) {
    listaCarrito.innerHTML = '<li>El carrito está vacío</li>';
  } else {
    let total = 0;  // Variable para calcular el total
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

      // Sumar el precio total
      total += producto.precio * producto.cantidad;
    });

    // Mostrar el total a pagar
    totalCarrito.innerHTML = `<strong>Total a pagar: $${total.toFixed(0)}</strong>`;
  }
}

// Función para eliminar un producto del carrito
function eliminarDelCarrito(index) {
  const carrito = JSON.parse(localStorage.getItem('carrito')) || [];
  
  // Eliminar el producto por su índice
  carrito.splice(index, 1);

  // Guardar el carrito actualizado
  localStorage.setItem('carrito', JSON.stringify(carrito));

  // Actualizar la vista del carrito
  mostrarCarrito();
}

// Función para vaciar el carrito
function vaciarCarrito() {
  // Eliminar todo el carrito
  localStorage.removeItem('carrito');

  // Actualizar la vista del carrito
  mostrarCarrito();
}
