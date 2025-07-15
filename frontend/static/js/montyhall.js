// Monty Hall Game Logic for juego.html
// Sonidos - Rutas corregidas para Flask
const audioOpenDoor = new Audio('/static/resources/OpenDoor.mp3');
const audioWin = new Audio('/static/resources/Win.mp3');
const audioFail = new Audio('/static/resources/Fail.mp3');

const doors = ['A', 'B', 'C'];
let premio = 0;
let picks = {};
let selectedDoor = null;
let openedDoor = null;
let gameEnded = false;
let ganadas = 0;
let perdidas = 0;

const presenterImg = document.getElementById('presenter');
const doorImgs = {
    'A': document.getElementById('doorA'),
    'B': document.getElementById('doorB'),
    'C': document.getElementById('doorC')
};
const messageDiv = document.getElementById('message');
const statsDiv = document.getElementById('stats');
const restartBtn = document.getElementById('restart');

function inicializarJuego() {
    premio = Math.floor(Math.random() * 3);
    const back = ['Cabra', 'Cabra', 'Cabra'];
    back[premio] = 'Carro';
    picks = { 'A': back[0], 'B': back[1], 'C': back[2] };
    selectedDoor = null;
    openedDoor = null;
    gameEnded = false;

    // Crear y aplicar estilo al texto principal
    messageDiv.innerHTML = '';
    const txtContainer = document.createElement('div');
    txtContainer.className = 'txt-puerta';
    txtContainer.textContent = 'Selecciona una puerta.';
    messageDiv.appendChild(txtContainer);

    // Ruta corregida para Flask
    presenterImg.src = "/static/resources/Presentador1.jpeg";

    for (const d of doors) {
        // Ruta corregida para Flask
        doorImgs[d].src = '/static/resources/Puerta_estatica.png';
        doorImgs[d].classList.remove('selected');
        doorImgs[d].style.pointerEvents = 'auto';
    }
    restartBtn.style.display = 'none';
}

function actualizarStats() {
    const total = ganadas + perdidas;
    const pct = total > 0 ? (ganadas / total * 100).toFixed(2) : '0.00';
    statsDiv.textContent = `Ganadas: ${ganadas} | Perdidas: ${perdidas} | % de victorias: ${pct}%`;
}

function seleccionarPuerta(door) {
    if (gameEnded || selectedDoor) return;
    selectedDoor = door;
    doorImgs[door].classList.add('selected');
    messageDiv.textContent = `Has seleccionado la puerta ${door}. El presentador abrirá una puerta...`;

    // Buscar una puerta para abrir (que no sea la seleccionada y no tenga el premio)
    const disponibles = doors.filter(d => d !== door && picks[d] === 'Cabra');
    openedDoor = disponibles[Math.floor(Math.random() * disponibles.length)];

    // Mostrar animación de abrir puerta antes de mostrar la cabra - Ruta corregida
    doorImgs[openedDoor].src = '/static/resources/Puerta_abierta.png';
    audioOpenDoor.currentTime = 0;
    audioOpenDoor.play();
    setTimeout(() => abrirPuerta(openedDoor), 900);
}

function abrirPuerta(door) {
    // Ruta corregida para Flask
    doorImgs[door].src = '/static/resources/Cabra.gif';
    doorImgs[door].classList.remove('selected');
    doorImgs[door].style.pointerEvents = 'none';
    messageDiv.textContent = `El presentador abrió la puerta ${door} y mostró una cabra. ¿Deseas cambiar de puerta?`;
    mostrarBotonesCambio();
}

function mostrarBotonesCambio() {
    const btnContainer = document.createElement('div');
    btnContainer.className = 'change-btns';
    const btnSi = document.createElement('button');
    btnSi.textContent = 'Sí, cambiar';
    btnSi.className = 'btn-monty btn-white';
    const btnNo = document.createElement('button');
    btnNo.textContent = 'No, mantener';
    btnNo.className = 'btn-monty btn-white';
    btnContainer.appendChild(btnSi);
    btnContainer.appendChild(btnNo);
    messageDiv.appendChild(btnContainer);
    btnSi.onclick = () => finalizarJuego(true);
    btnNo.onclick = () => finalizarJuego(false);
}

function finalizarJuego(cambiar) {
    // Limpiar botones
    messageDiv.innerHTML = '';
    let finalDoor = selectedDoor;
    if (cambiar) {
        finalDoor = doors.find(d => d !== selectedDoor && d !== openedDoor);
        doorImgs[selectedDoor].classList.remove('selected');
        doorImgs[finalDoor].classList.add('selected');
    }

    // Mostrar premios - Rutas corregidas
    for (const d of doors) {
        if (picks[d] === 'Carro') {
            doorImgs[d].src = '/static/resources/carro.gif';
        } else {
            doorImgs[d].src = '/static/resources/Cabra.gif';
        }
        doorImgs[d].style.pointerEvents = 'none';
    }

    // Resultado - Rutas corregidas
    if (picks[finalDoor] === 'Carro') {
        presenterImg.src = '/static/resources/Presentador1.jpeg';
        messageDiv.textContent = `¡Felicidades! Ganaste el carro en la puerta ${finalDoor}.`;
        ganadas++;
        audioWin.currentTime = 0;
        audioWin.play();
    } else {
        presenterImg.src = '/static/resources/Presentador2.jpeg';
        messageDiv.textContent = `Lo siento, encontraste una cabra en la puerta ${finalDoor}.`;
        perdidas++;
        audioFail.currentTime = 0;
        audioFail.play();
    }

    actualizarStats();
    gameEnded = true;
    restartBtn.style.display = 'inline-block';
}

// Event listeners
for (const d of doors) {
    doorImgs[d].addEventListener('click', () => seleccionarPuerta(d));
}
restartBtn.addEventListener('click', () => {
    inicializarJuego();
});

// Inicializar el juego
inicializarJuego();
actualizarStats();