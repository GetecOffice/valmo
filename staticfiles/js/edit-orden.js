
var checkboxContainer = document.getElementById('checkboxContainer');
var accessoryInput = document.getElementById('accesorioInput');

checkboxContainer.addEventListener('change', function (event) {
    var checkboxes = checkboxContainer.querySelectorAll('input[type="checkbox"]:checked');
    var selectedAccessories = [];

    checkboxes.forEach(function (checkbox) {
        selectedAccessories.push(checkbox.value);
    });

    accessoryInput.value = selectedAccessories.join(', ');
});


var jq = $.noConflict(); // Guarda la referencia a jQuery en una variable diferente

jq(document).ready(function () {
    var select = jq('#accesorioSelect');
    var input = jq('#accesorioInput');

    select.select2();

    select.on('change', function () {
        var selectedOptions = select.val();
        var selectedTexts = select.find('option:selected').map(function () {
            return jq(this).text();
        }).get();

        input.val(selectedTexts.join(', '));
    });

    jq('.select2').select2();
});


// Obtener referencia al campo de entrada
const fechaInput = document.getElementById('fecha-input');
const fechaInput2 = document.getElementById('fecha-input2');
// Obtener la fecha y hora actual
const fechaActual = new Date();

// Convertir la fecha y hora actual a una cadena con zona horaria
const fechaConZonaHoraria = fechaActual.toLocaleString('sv-SE', { timeZone: 'America/Tijuana' });

// Quitar los microsegundos
const fechaSinMicrosegundos = fechaConZonaHoraria.slice(0, 16);

// Establecer el valor en el campo de entrada
fechaInput.value = fechaSinMicrosegundos;
fechaInput2.value = fechaSinMicrosegundos;

<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>


document.addEventListener("DOMContentLoaded", function () {
    const fileInputs = document.querySelectorAll(".src-file1");

    fileInputs.forEach(function (input, index) {
        input.addEventListener("change", function (event) {
            const fileName = event.target.files[0].name;
            const label = event.target.nextElementSibling;
            const preview = document.getElementById(`preview${index + 1}`);

            label.textContent = fileName;

            if (event.target.files && event.target.files[0]) {
                const reader = new FileReader();

                reader.onload = function (e) {
                    preview.src = e.target.result;
                    preview.style.display = "block";
                };

                reader.readAsDataURL(event.target.files[0]);

                // Ocultar las imágenes existentes al seleccionar una nueva imagen
                $(input).closest('.select-orden-trabajo').find('img[id^="imagen"]').hide();
            }
        });
    });
});

function mostrarImagen(imagen) {
    var contenedor = document.createElement("div");
    contenedor.setAttribute("id", "imagen-fullscreen");

    var imagenFullscreen = document.createElement("img");
    imagenFullscreen.setAttribute("src", imagen.src);

    contenedor.appendChild(imagenFullscreen);
    document.body.appendChild(contenedor);

    function removerContenedor() {
        contenedor.remove();
        document.removeEventListener("click", removerContenedor);
        document.removeEventListener("keydown", removerContenedorOnEsc);
    }

    contenedor.addEventListener("click", removerContenedor);

    function removerContenedorOnEsc(event) {
        if (event.key === "Escape") {
            removerContenedor();
        }
    }

    document.addEventListener("keydown", removerContenedorOnEsc);
}
