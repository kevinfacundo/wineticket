const eventos = [
    { id: 1, nombre: "Vendimia 2024", img: '/static/images/SUNSET BODEGA LOPEZ.jpg' },
    { id: 2, nombre: "Vino el cine", img: 'static/images/BODEGA LOPEZ 2.jpeg' },
    { id: 3, nombre: "Expo wine hilton", img: 'static/images/BODEGA LOPEZ 3.jpeg' }
];

const card = document.getElementById('card-event');
const next = document.getElementById('btn-next-event');
const prev = document.getElementById('btn-prev-event');
let currentEvent = 0;

window.addEventListener('DOMContentLoaded', () => {
    showEvent(currentEvent);
});

const showEvent = (e) => {
    const event = eventos[e];
    const url = event.img;
    card.style.opacity = 0;
    setTimeout(() => {
        card.src = url;
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