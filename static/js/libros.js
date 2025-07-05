document.addEventListener("DOMContentLoaded", function () {

  // Delegación para botón Editar: reemplaza contenido principal
  document.addEventListener("click", function (e) {
    if (e.target.closest(".btn-editar")) {
      const btn = e.target.closest(".btn-editar");
      const libroId = btn.getAttribute("data-id");

      const contenedor = document.getElementById("contenido-principal");
      contenedor.innerHTML = `
        <div class="d-flex justify-content-center align-items-center p-4">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Cargando...</span>
          </div>
        </div>
      `;

      fetch(`/admin/libros/editar/${libroId}`)
        .then(res => res.text())
        .then(html => {
          contenedor.innerHTML = html;
          contenedor.style.opacity = 0;
          contenedor.style.transition = "opacity 0.3s ease";
          setTimeout(() => contenedor.style.opacity = 1, 10);
        });
    }
  });

  // Filtro tabla
  document.getElementById("busqueda-libro").addEventListener("keyup", function () {
    const filtro = this.value.toLowerCase();
    const filas = document.querySelectorAll("#tabla-libros tbody tr");

    filas.forEach(fila => {
      const titulo = fila.dataset.titulo;
      const autor = fila.dataset.autor;
      const isbn = fila.dataset.isbn;
      const categoria = fila.dataset.categoria;
      const coincide = titulo.includes(filtro) || autor.includes(filtro) || isbn.includes(filtro) || categoria.includes(filtro);
      fila.style.display = coincide ? "" : "none";
    });
  });
});
