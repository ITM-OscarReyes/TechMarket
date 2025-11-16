// static/main.js
async function cargarProductos() {
  const res = await fetch("/api/products");
  const productos = await res.json();
  const tbody = document.querySelector("#tabla-productos tbody");
  tbody.innerHTML = "";

  productos.forEach(p => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${p.id}</td>
      <td>${p.name}</td>
      <td>${p.description}</td>
      <td>${p.price}</td>
      <td>${p.quantity}</td>
      <td>
        ${currentRole === 'admin' ? `<a class="btn btn-sm btn-warning me-1" href="/products/edit/${p.id}">Editar</a>
        <button class="btn btn-sm btn-danger" onclick="borrar(${p.id})">Eliminar</button>` : ''}
      </td>
    `;
    tbody.appendChild(tr);
  });
}

async function borrar(id) {
  if (!confirm("¿Eliminar producto?")) return;
  const res = await fetch(`/api/products/${id}`, { method: "DELETE" });
  const j = await res.json();
  alert(j.message);
  if (res.status === 200) cargarProductos();
}

document.addEventListener("DOMContentLoaded", () => {
  if (document.querySelector("#tabla-productos")) {
    cargarProductos();
  }
});
