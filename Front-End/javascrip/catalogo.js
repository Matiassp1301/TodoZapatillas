// Simulación de datos tipo "base de datos"
const productos = [
  {
    id: 1,
    nombre: "Zapatilla Running Mujer",
    descripcion: "Zapatilla cómoda y ligera para correr en ciudad o campo.",
    imagen: "https://segurycel.vteximg.com.br/arquivos/ids/158009-475-475/7243503020205539.jpg?v=638766079765370000",
    imagenesExtras: [
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSGVhPmzmL1NJc4P5VXuwumTEo4XrwVv-LrlA&s",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSGVhPmzmL1NJc4P5VXuwumTEo4XrwVv-LrlA&s",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSGVhPmzmL1NJc4P5VXuwumTEo4XrwVv-LrlA&s"
    ],
    proveedores: [
      { nombre: "Tienda A", precio: 39990 },
      { nombre: "Tienda B", precio: 38990 }
    ],
    colores: ["Negro", "Rosa", "Blanco"],
    tallas: [36, 37, 38, 39]
  },
  {
    id: 2,
    nombre: "Zapatilla Urbana Hombre",
    descripcion: "Diseño moderno y resistente para uso diario urbano.",
    imagen: "https://segurycel.vteximg.com.br/arquivos/ids/158009-475-475/7243503020205539.jpg?v=638766079765370000",
    proveedores: [
      { nombre: "Tienda C", precio: 49990 }
    ],
    colores: ["red", "black"],
    tallas: [40, 41, 42]
  },
  {
    id: 3,
    nombre: "Zapatilla Deportiva Niño",
    descripcion: "Ideal para niños activos, con suela antideslizante.",
    imagen: "https://segurycel.vteximg.com.br/arquivos/ids/158009-475-475/7243503020205539.jpg?v=638766079765370000",
    proveedores: [
      { nombre: "Tienda D", precio: 29990 }
    ],
    colores: ["Azul", "Rojo"],
    tallas: [30, 31, 32]
  }
];

// Mostrar catálogo
const catalogo = document.getElementById('catalogo');
if (catalogo) {
  productos.forEach(producto => {
    const card = document.createElement('div');
    card.classList.add('card');
    card.innerHTML = `
      <img src="${producto.imagen}" alt="${producto.nombre}">
      <div class="card-content">
        <h3>${producto.nombre}</h3>
        <p class="price">Desde $${Math.min(...producto.proveedores.map(p => p.precio)).toLocaleString()}</p>
      </div>
    `;
    card.onclick = () => {
      localStorage.setItem('productoSeleccionado', JSON.stringify(producto));
      window.location.href = 'detalle.html';
    };
    catalogo.appendChild(card);
  });
}
//Traducir el nombre del color 
function traducirColor(nombre) {
  const mapa = {
    'Negro': 'black',
    'Blanco': 'white',
    'Rojo': 'red',
    'Rosa': 'pink',
    'Gris': 'gray',
    'Azul': 'blue',
    'Verde': 'green',
    'Amarillo': 'yellow',
    'Café': 'saddlebrown',
    'Marrón': 'brown',
    'Beige': 'beige',
    'Celeste': 'skyblue',
    'Lila': 'plum',
    'Morado': 'purple',
    'Naranja': 'orange',
    'Fucsia': 'fuchsia',
    'Turquesa': 'turquoise',
    'Dorado': 'gold',
    'Plateado': 'silver',
    'Vino': 'darkred',
    'Oliva': 'olive'
  };
  return mapa[nombre] || nombre.toLowerCase(); // Si no está en el mapa, usa minúscula
}


// Mostrar detalle
const detalle = document.getElementById('producto-detalle');
if (detalle) {
  const producto = JSON.parse(localStorage.getItem('productoSeleccionado'));
  if (producto) {
    // Radios para proveedores (con nombre y precio)
      const proveedorRadios = producto.proveedores.map((p, i) => `
        <input type="radio" id="proveedor-${i}" name="proveedor" value="${p.nombre}" ${i === 0 ? 'checked' : ''}>
        <label for="proveedor-${i}">${p.nombre} — $${p.precio.toLocaleString()}</label>
      `).join('');

      // Radios para colores
      const colorRadios = producto.colores.map((color, i) => {
        const colorCSS = traducirColor(color);
        return `
          <input type="radio" id="color-${i}" name="color" value="${color}" ${i === 0 ? 'checked' : ''} class="input-color">
          <label for="color-${i}" class="label-color" style="background-color: ${colorCSS};" title="${color}"></label>
        `;
      }).join('');


      // Radios para tallas
      const tallaRadios = producto.tallas.map((talla, i) => `
        <input type="radio" id="talla-${i}" name="talla" value="${talla}" ${i === 0 ? 'checked' : ''}>
        <label for="talla-${i}">${talla}</label>
      `).join('');

        // Aquí generamos miniaturas
      const imagenesMiniaturas = [producto.imagen, ...(producto.imagenesExtras || [])];
      const miniaturasHTML = imagenesMiniaturas.map((imgSrc, i) => `
        <img src="${imgSrc}" class="miniatura" alt="Imagen ${i + 1}" style="cursor:pointer; width: 60px; height: 60px; object-fit: cover; margin-right: 5px; border: 2px solid transparent;">
      `).join('');

      detalle.innerHTML = `
        <div class="detalle-container">
          <div class="detalle-imagen-container">
          <img id="imagen-principal" class="detalle-imagen" src="${producto.imagen}" alt="${producto.nombre}" />
          <div class="miniaturas-container">
            ${miniaturasHTML}
          </div>
        </div>
          <div class="detalle-info">
            <h1>${producto.nombre}</h1>

            <fieldset class="product-form__input variant-input-wrapper">
              <legend class="form__label">Proveedor</legend>
              ${proveedorRadios}
            </fieldset>

            <fieldset class="product-form__input variant-input-wrapper">
              <legend class="form__label">Color</legend>
              ${colorRadios}
            </fieldset>

            <fieldset class="product-form__input variant-input-wrapper">
              <legend class="form__label">Talla</legend>
              ${tallaRadios}
            </fieldset>

            <div class="opciones">
              <label for="cantidad-seleccionada">Cantidad:</label>
              <input type="number" id="cantidad-seleccionada" class="input-cantidad" value="1" min="1">
            </div>

            <div class="botones">
              <button class="boton carrito-b" onclick="agregarAlCarrito(${producto.id})">Agregar al Carrito</button>
            </div>
          </div>
        </div>

        <div class="detalle-descripcion">
          <p>${producto.descripcion}</p>
        </div>
      `;
      // en botones poner despues 
      //       <button class="boton " >Comprar</button>
      //       <button class="boton " >Favorito ♡</button>

      const imagenPrincipal = document.getElementById('imagen-principal');
          const miniaturas = document.querySelectorAll('.miniatura');

          miniaturas.forEach(miniatura => {
            miniatura.addEventListener('click', () => {
              imagenPrincipal.src = miniatura.src;
              miniaturas.forEach(m => m.style.border = '2px solid transparent'); // Quitar borde
              miniatura.style.border = '2px solid #000'; // Poner borde al seleccionado
            });
          });

          if(miniaturas.length > 0) {
            miniaturas[0].style.border = '2px solid #000';
          }

        } else {
          detalle.innerHTML = `<p>Producto no encontrado.</p>`;
        }
      }


