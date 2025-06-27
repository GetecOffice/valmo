function checkInputValidity(input, errorMessageId, agregarBotonId, salirBotonId) {
    const agregarBoton = document.getElementById(agregarBotonId);
    const salirBoton = document.getElementById(salirBotonId);

    if (input.value.includes('.')) {
        input.classList.add('is-invalid');
        document.getElementById(errorMessageId).style.display = 'block';
        agregarBoton.disabled = true;
        salirBoton.disabled = true;
    } else {
        input.classList.remove('is-invalid');
        document.getElementById(errorMessageId).style.display = 'none';
        agregarBoton.disabled = false;
        salirBoton.disabled = false;
    }
}