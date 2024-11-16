document.addEventListener('DOMContentLoaded', () => {
    const filterInput = document.querySelector('input[name="Buscar"]');
    const categorySelect = document.getElementById('categories');
    const dateInput = document.querySelector('input[type="date"]');
    const eventCards = document.querySelectorAll('.event-card');

    // Establecer límites de fecha para el input de tipo date
    const currentYear = new Date().getFullYear();
    dateInput.min = `${currentYear}-01-01`; // Primer día del año
    dateInput.max = `${currentYear}-12-31`; // Último día del año

    // Filtrar eventos
    function filterEvents() {
        const searchText = filterInput.value.toLowerCase().trim();
        const selectedCategory = categorySelect.value.toLowerCase();
        const selectedDate = dateInput.value;

        eventCards.forEach(card => {
            const title = card.querySelector('h3').textContent.toLowerCase();
            const category = card.querySelector('p').textContent.toLowerCase();
            const eventDate = card.querySelector('input[type="date"]').value;

            const matchesSearch = title.includes(searchText);
            const matchesCategory = selectedCategory ? category.includes(selectedCategory) : true;
            const matchesDate = selectedDate ? selectedDate === eventDate : true;

            // Mostrar u ocultar el evento basado en las coincidencias
            if (matchesSearch && matchesCategory && matchesDate) {
                card.style.display = ''; // Mostrar evento
            } else {
                card.style.display = 'none'; // Ocultar evento
            }
        });
    }

    // Asignar los eventos de filtrado
    filterInput.addEventListener('input', filterEvents);
    categorySelect.addEventListener('change', filterEvents);
    dateInput.addEventListener('change', filterEvents);
});
