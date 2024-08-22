document.addEventListener('DOMContentLoaded', function () {

    new TomSelect('#areas', {
        hidePlaceholder: true,
        plugins: [
            'remove_button',
            'clear_button',
            'optgroup_columns',
        ],
        maxOptions: null,
    });
    
    new TomSelect('#amenities', {
        hidePlaceholder: true,
        plugins: [
            'remove_button',
            'clear_button',
        ],
    });

    const form = document.querySelector('.needs-validation');
    form.addEventListener('submit', function (event) {
        if (form.checkValidity() === false) {
            event.preventDefault();
            event.stopPropagation();
        }
        form.classList.add('was-validated');
    }, false);

});