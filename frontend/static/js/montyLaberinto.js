// Monty Hall Game Logic for Laberinto - Versión con imágenes y sonidos
// Mantiene todas las características visuales del código original

// Sonidos - Rutas para Flask
const audioOpenDoor = new Audio('/static/resources/OpenDoor.mp3');
const audioWin = new Audio('/static/resources/Win.mp3');
const audioFail = new Audio('/static/resources/Fail.mp3');

// Variables globales para el juego Monty Hall
let montyHallGame = {
    doors: ['A', 'B', 'C'],
    premio: 0,
    picks: {},
    selectedDoor: null,
    openedDoor: null,
    gameEnded: false,
    callback: null,
    ganadas: 0,
    perdidas: 0
};

// Función principal para mostrar el modal de Monty Hall
function showMontyHall(callback) {
    const modal = document.getElementById("monty-modal");

    // Limpiar modal anterior y crear estructura nueva
    modal.innerHTML = `
        <div style="
            background: #fff;
            padding: 30px;
            border-radius: 10px;
            min-width: 500px;
            max-width: 800px;
            text-align: center;
            position: relative;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        ">
            <h3 style="margin-bottom: 20px; color: #333;">¡Juego Monty Hall!</h3>
            
            <!-- Imagen del presentador -->
            <div style="margin-bottom: 20px;">
                <img id="presenter" src="/static/resources/Presentador1.jpeg" 
                     alt="Presentador" style="width: 120px; height: 120px; border-radius: 10px;">
            </div>
            
            <!-- Mensaje principal -->
            <div id="monty-message" style="margin: 20px 0; min-height: 60px; font-size: 1.1em;">
                <div class="txt-puerta" style="color: #333; font-weight: bold;">
                    Selecciona una puerta.
                </div>
            </div>
            
            <!-- Puertas -->
            <div id="monty-doors" style="
                display: flex;
                justify-content: center;
                gap: 30px;
                margin: 30px 0;
                align-items: center;
            "></div>
            
            <!-- Estadísticas -->
            <div id="stats" style="
                margin: 20px 0;
                padding: 10px;
                background: #f5f5f5;
                border-radius: 5px;
                font-size: 0.9em;
                color: #666;
            "></div>
            
            <!-- Botones de control -->
            <div style="margin-top: 20px;">
                <button id="monty-close" style="
                    display: none;
                    padding: 10px 20px;
                    background: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 1em;
                ">Cerrar</button>
                
                <button id="restart-monty" style="
                    display: none;
                    padding: 10px 20px;
                    background: #2196F3;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 1em;
                    margin-left: 10px;
                ">Jugar de nuevo</button>
            </div>
        </div>
    `;

    // Mostrar modal
    modal.style.display = "flex";

    // Inicializar juego
    inicializarMontyHall(callback);

    // Configurar controles de voz
    configurarVozMontyHall();

    // Crear puertas con imágenes
    crearPuertasConImagenes();

    // Actualizar estadísticas
    actualizarStats();
}

// Inicializar el juego Monty Hall
function inicializarMontyHall(callback) {
    montyHallGame.premio = Math.floor(Math.random() * 3);
    const back = ['Cabra', 'Cabra', 'Cabra'];
    back[montyHallGame.premio] = 'Carro';
    montyHallGame.picks = { 'A': back[0], 'B': back[1], 'C': back[2] };
    montyHallGame.selectedDoor = null;
    montyHallGame.openedDoor = null;
    montyHallGame.gameEnded = false;
    montyHallGame.callback = callback;

    // Resetear presentador
    const presenter = document.getElementById('presenter');
    if (presenter) {
        presenter.src = "/static/resources/Presentador1.jpeg";
    }
}

// Crear puertas con imágenes
function crearPuertasConImagenes() {
    const doorsDiv = document.getElementById("monty-doors");
    doorsDiv.innerHTML = "";

    montyHallGame.doors.forEach((door, index) => {
        const doorContainer = document.createElement("div");
        doorContainer.style = "display: flex; flex-direction: column; align-items: center; cursor: pointer;";

        const doorImg = document.createElement("img");
        doorImg.src = "/static/resources/Puerta_estatica.png";
        doorImg.alt = `Puerta ${door}`;
        doorImg.style = "width: 120px; height: 160px; border: 3px solid #ccc; border-radius: 10px; transition: all 0.3s ease;";
        doorImg.id = `door${door}`;

        const doorLabel = document.createElement("div");
        doorLabel.textContent = `Puerta ${door}`;
        doorLabel.style = "margin-top: 10px; font-weight: bold; font-size: 1.1em;";

        doorContainer.appendChild(doorImg);
        doorContainer.appendChild(doorLabel);

        // Evento de click
        doorContainer.onclick = () => seleccionarPuertaMonty(index);

        // Efecto hover
        doorContainer.onmouseenter = () => {
            if (!montyHallGame.gameEnded && montyHallGame.selectedDoor === null) {
                doorImg.style.borderColor = "#4CAF50";
                doorImg.style.transform = "scale(1.05)";
            }
        };

        doorContainer.onmouseleave = () => {
            if (!montyHallGame.gameEnded && montyHallGame.selectedDoor !== index) {
                doorImg.style.borderColor = "#ccc";
                doorImg.style.transform = "scale(1)";
            }
        };

        doorsDiv.appendChild(doorContainer);
    });
}

// Seleccionar puerta en Monty Hall
function seleccionarPuertaMonty(index) {
    if (montyHallGame.gameEnded || montyHallGame.selectedDoor !== null) return;

    const door = montyHallGame.doors[index];
    montyHallGame.selectedDoor = index;

    const doorImg = document.getElementById(`door${door}`);
    const messageDiv = document.getElementById("monty-message");

    // Marcar puerta seleccionada
    doorImg.style.borderColor = "#4CAF50";
    doorImg.style.borderWidth = "4px";
    doorImg.style.transform = "scale(1.05)";

    messageDiv.innerHTML = `<div style="color: #333; font-weight: bold;">Has seleccionado la puerta ${door}. El presentador abrirá una puerta...</div>`;

    // Buscar una puerta para abrir (que no sea la seleccionada y no tenga el premio)
    const disponibles = montyHallGame.doors
        .map((_, idx) => idx)
        .filter((idx) => idx !== index && montyHallGame.picks[montyHallGame.doors[idx]] === 'Cabra');

    montyHallGame.openedDoor = disponibles[Math.floor(Math.random() * disponibles.length)];

    // Animar apertura de puerta
    setTimeout(() => abrirPuertaConAnimacion(montyHallGame.openedDoor), 1500);
}

// Abrir puerta con animación
function abrirPuertaConAnimacion(doorIndex) {
    const door = montyHallGame.doors[doorIndex];
    const doorImg = document.getElementById(`door${door}`);
    const messageDiv = document.getElementById("monty-message");

    // Mostrar animación de abrir puerta
    doorImg.src = '/static/resources/Puerta_abierta.png';
    doorImg.style.borderColor = "#ff9800";

    // Reproducir sonido
    audioOpenDoor.currentTime = 0;
    audioOpenDoor.play();

    // Después de la animación, mostrar la cabra
    setTimeout(() => {
        doorImg.src = '/static/resources/Cabra.gif';
        doorImg.style.borderColor = "#f44336";

        messageDiv.innerHTML = `<div style="color: #333; font-weight: bold;">El presentador abrió la puerta ${door} y mostró una cabra.<br>¿Deseas cambiar de puerta?</div>`;

        // Mostrar botones de cambio
        mostrarBotonesCambio();
    }, 900);
}

// Mostrar botones de cambiar o mantener
function mostrarBotonesCambio() {
    const messageDiv = document.getElementById("monty-message");

    const btns = document.createElement("div");
    btns.style = "margin-top: 20px; display: flex; gap: 15px; justify-content: center;";

    const btnCambiar = document.createElement("button");
    btnCambiar.textContent = "Sí, cambiar";
    btnCambiar.className = "btn-monty";
    btnCambiar.style = `
        padding: 12px 25px;
        font-size: 1.1em;
        background: #2196F3;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.3s ease;
    `;
    btnCambiar.onmouseover = () => btnCambiar.style.background = "#1976D2";
    btnCambiar.onmouseout = () => btnCambiar.style.background = "#2196F3";
    btnCambiar.onclick = () => finalizarMontyHall(true);

    const btnMantener = document.createElement("button");
    btnMantener.textContent = "No, mantener";
    btnMantener.className = "btn-monty";
    btnMantener.style = `
        padding: 12px 25px;
        font-size: 1.1em;
        background: #FF9800;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.3s ease;
    `;
    btnMantener.onmouseover = () => btnMantener.style.background = "#F57C00";
    btnMantener.onmouseout = () => btnMantener.style.background = "#FF9800";
    btnMantener.onclick = () => finalizarMontyHall(false);

    btns.appendChild(btnCambiar);
    btns.appendChild(btnMantener);
    messageDiv.appendChild(btns);
}

// Finalizar el juego Monty Hall
function finalizarMontyHall(cambiar) {
    const messageDiv = document.getElementById("monty-message");
    const presenter = document.getElementById('presenter');
    const closeBtn = document.getElementById("monty-close");
    const restartBtn = document.getElementById("restart-monty");

    // Limpiar botones
    const btns = messageDiv.querySelectorAll('.btn-monty');
    btns.forEach(btn => btn.remove());

    let finalDoor = montyHallGame.selectedDoor;
    if (cambiar) {
        // Cambiar selección
        const oldDoor = montyHallGame.doors[montyHallGame.selectedDoor];
        const oldDoorImg = document.getElementById(`door${oldDoor}`);
        oldDoorImg.style.borderColor = "#ccc";
        oldDoorImg.style.transform = "scale(1)";

        finalDoor = [0, 1, 2].find((idx) => idx !== montyHallGame.selectedDoor && idx !== montyHallGame.openedDoor);

        const newDoor = montyHallGame.doors[finalDoor];
        const newDoorImg = document.getElementById(`door${newDoor}`);
        newDoorImg.style.borderColor = "#4CAF50";
        newDoorImg.style.borderWidth = "4px";
        newDoorImg.style.transform = "scale(1.05)";
    }

    // Mostrar todos los premios
    montyHallGame.doors.forEach((door, idx) => {
        const doorImg = document.getElementById(`door${door}`);
        if (idx !== montyHallGame.openedDoor) {
            if (montyHallGame.picks[door] === 'Carro') {
                doorImg.src = '/static/resources/carro.gif';
                doorImg.style.borderColor = "#FFD700";
                doorImg.style.borderWidth = "4px";
            } else {
                doorImg.src = '/static/resources/Cabra.gif';
                doorImg.style.borderColor = "#f44336";
            }
        }
    });

    // Mostrar resultado
    const finalPrize = montyHallGame.picks[montyHallGame.doors[finalDoor]];
    const ganaste = finalPrize === "Carro";

    if (ganaste) {
        presenter.src = '/static/resources/Presentador1.jpeg';
        messageDiv.innerHTML = `<div style="color: #4CAF50; font-weight: bold; font-size: 1.3em;">¡Felicidades! Ganaste el carro en la puerta ${montyHallGame.doors[finalDoor]}.<br>Puedes continuar en el laberinto.</div>`;
        montyHallGame.ganadas++;
        audioWin.currentTime = 0;
        audioWin.play();
    } else {
        presenter.src = '/static/resources/Presentador2.jpeg';
        messageDiv.innerHTML = `<div style="color: #f44336; font-weight: bold; font-size: 1.3em;">Lo siento, encontraste una cabra en la puerta ${montyHallGame.doors[finalDoor]}.<br>Regresarás al inicio del laberinto.</div>`;
        montyHallGame.perdidas++;
        audioFail.currentTime = 0;
        audioFail.play();
    }

    // Actualizar estadísticas
    actualizarStats();

    // Mostrar botones
    closeBtn.style.display = "inline-block";
    restartBtn.style.display = "inline-block";

    closeBtn.onclick = () => cerrarModalMontyHall(ganaste);
    restartBtn.onclick = () => reiniciarJuego();

    montyHallGame.gameEnded = true;
}

// Actualizar estadísticas
function actualizarStats() {
    const statsDiv = document.getElementById("stats");
    if (statsDiv) {
        const total = montyHallGame.ganadas + montyHallGame.perdidas;
        const pct = total > 0 ? (montyHallGame.ganadas / total * 100).toFixed(2) : '0.00';
        statsDiv.innerHTML = `
            <strong>Estadísticas:</strong> 
            Ganadas: <span style="color: #4CAF50;">${montyHallGame.ganadas}</span> | 
            Perdidas: <span style="color: #f44336;">${montyHallGame.perdidas}</span> | 
            % de victorias: <span style="color: #2196F3;">${pct}%</span>
        `;
    }
}

// Reiniciar juego
function reiniciarJuego() {
    inicializarMontyHall(montyHallGame.callback);
    crearPuertasConImagenes();
    actualizarStats();

    const messageDiv = document.getElementById("monty-message");
    messageDiv.innerHTML = '<div class="txt-puerta" style="color: #333; font-weight: bold;">Selecciona una puerta.</div>';

    document.getElementById("monty-close").style.display = "none";
    document.getElementById("restart-monty").style.display = "none";
}

// Cerrar modal y ejecutar callback
function cerrarModalMontyHall(ganaste) {
    const modal = document.getElementById("monty-modal");
    modal.style.display = "none";

    // Limpiar handlers de voz
    limpiarVozMontyHall();

    // Ejecutar callback con resultado
    if (montyHallGame.callback) {
        montyHallGame.callback(ganaste);
    }
}

// Configurar controles de voz para Monty Hall
function configurarVozMontyHall() {
    window.montyVoice = window.montyVoice || {};

    window.montyVoice.selectDoor = (idx) => {
        if (montyHallGame.selectedDoor !== null) return;
        seleccionarPuertaMonty(idx);
    };

    window.montyVoice.selectAction = (cambiar) => {
        if (montyHallGame.selectedDoor === null || montyHallGame.gameEnded) return;
        finalizarMontyHall(cambiar);
    };

    window.montyVoice.closeModal = () => {
        const closeBtn = document.getElementById("monty-close");
        if (closeBtn && closeBtn.style.display !== "none") {
            closeBtn.click();
        }
    };

    window.montyVoice.restartGame = () => {
        const restartBtn = document.getElementById("restart-monty");
        if (restartBtn && restartBtn.style.display !== "none") {
            restartBtn.click();
        }
    };
}

// Limpiar handlers de voz
function limpiarVozMontyHall() {
    if (window.montyVoice) {
        window.montyVoice.selectDoor = null;
        window.montyVoice.selectAction = null;
        window.montyVoice.closeModal = null;
        window.montyVoice.restartGame = null;
    }
}

// Manejar errores de carga de imágenes
document.addEventListener('DOMContentLoaded', function() {
    // Precargar imágenes
    const imagesToPreload = [
        '/static/resources/Presentador1.jpeg',
        '/static/resources/Presentador2.jpeg',
        '/static/resources/Puerta_estatica.png',
        '/static/resources/Puerta_abierta.png',
        '/static/resources/Cabra.gif',
        '/static/resources/carro.gif'
    ];

    imagesToPreload.forEach(src => {
        const img = new Image();
        img.src = src;
    });
});

// Exportar funciones principales si se usa como módulo
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        showMontyHall,
        inicializarMontyHall,
        seleccionarPuertaMonty,
        finalizarMontyHall
    };
}