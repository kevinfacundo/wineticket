const eventos = [
    { id: 1, nombre: "Vendimia 2024", img: 'static/images/VENDIMIA 2024.png', link: '/vendimia' },
    { id: 2, nombre: "Vino el cine", img: 'static/images/VINO EL CINE.jpg', link: '/vino_el_cine' },
    { id: 3, nombre: "Expo wine hilton", img: 'static/images/EXPO WINE HILTON.jpg', link: '/expo_wine_hilton' }
];

const card = document.getElementById('card');
const cardLink = document.getElementById('card-link');
const next = document.getElementById('btn-next');
const prev = document.getElementById('btn-prev');
let currentEvent = 0;

window.addEventListener('DOMContentLoaded', () => {
    showEvent(currentEvent);
});

const showEvent = (e) => {
    const event = eventos[e];
    const url = event.img;
    const link = event.link;
    card.style.opacity = 0;
    setTimeout(() => {
        card.src = url;
        cardLink.href = link;  // Actualiza el enlace dinámicamente
        card.style.opacity = 1;
    }, 250);
};

const handleNext = () => {
    currentEvent++;
    if (currentEvent >= eventos.length) {
        currentEvent = 0;
    }
    showEvent(currentEvent);
};

setInterval(handleNext, 5000);
next.addEventListener('click', handleNext);

const handlePrev = () => {
    currentEvent--;
    if (currentEvent < 0) {
        currentEvent = eventos.length - 1;
    }
    showEvent(currentEvent);
};

prev.addEventListener('click', handlePrev);
