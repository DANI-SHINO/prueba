document.addEventListener("DOMContentLoaded", () => {
  const tabla = document.getElementById("tabla-usuarios");

  tabla.addEventListener("click", (event) => {
    const target = event.target;

    // 👉 Botón editar
    if (target.closest(".btn-editar-usuario")) {
      const btn = target.closest(".btn-editar-usuario");
      const userId = btn.getAttribute("data-id");
      console.log(`Editar usuario ID: ${userId}`);

      // ⚡ Traer formulario y reemplazar todo el body
      fetch(`/admin/usuarios/editar_formulario/${userId}`)
        .then(res => res.text())
        .then(html => {
          document.body.innerHTML = html;

          // ✅ Inyectar de nuevo el script del formulario
          const newScript = document.createElement("script");
          newScript.textContent = `
            document.getElementById("form-editar-usuario").addEventListener("submit", function (e) {
              e.preventDefault();
              const datos = {
                id: this.querySelector('[name="id"]').value,
                nombre: this.querySelector('[name="nombre"]').value,
                correo: this.querySelector('[name="correo"]').value,
                direccion: this.querySelector('[name="direccion"]').value,
                rol: this.querySelector('[name="rol"]').value
              };
              console.log("DEBUG:", datos);
              fetch("/admin/usuarios/editar", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(datos)
              })
              .then(res => res.json())
              .then(data => {
                alert(data.mensaje || "Usuario actualizado correctamente");
                window.location.href = "/admin/usuarios/mostrar";
              })
              .catch(err => {
                console.error("Error:", err);
                alert("Error inesperado");
              });
            });

            document.querySelector(".btn-cancelar-usuario").addEventListener("click", function () {
              window.location.href = "/admin/usuarios/mostrar";
            });
          `;
          document.body.appendChild(newScript);
        })
        .catch(err => {
          console.error("Error cargando formulario:", err);
        });
    }

    // 👉 Botón eliminar
    if (target.closest(".btn-eliminar-usuario")) {
      const btn = target.closest(".btn-eliminar-usuario");
      const userId = btn.getAttribute("data-id");
      if (confirm("¿Estás seguro de eliminar este usuario?")) {
        fetch(`/admin/usuarios/eliminar/${userId}`, { method: "POST" })
          .then(res => res.json())
          .then(data => {
            if (data.success) {
              alert("Usuario eliminado");
              location.reload();
            } else {
              alert("Error al eliminar");
            }
          })
          .catch(err => {
            console.error("Error eliminando usuario:", err);
          });
      }
    }
  });

  // 👉 Buscador de usuarios
  const inputBusqueda = document.getElementById("busqueda-usuario");
  inputBusqueda.addEventListener("keyup", () => {
    const filtro = inputBusqueda.value.toLowerCase();
    document.querySelectorAll("#tabla-usuarios tbody tr").forEach((fila) => {
      const texto = fila.textContent.toLowerCase();
      fila.style.display = texto.includes(filtro) ? "" : "none";
    });
  });
});
