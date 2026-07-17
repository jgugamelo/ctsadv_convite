/* ==========================================================================
   Sistema de Partículas (Background Dinâmico e Interativo)
   ========================================================================== */
const canvas = document.getElementById('particles-canvas');
const ctx = canvas.getContext('2d');

let particlesArray = [];
const mouse = {
    x: null,
    y: null,
    radius: 120 // Raio de atração do mouse
};

// Captura do movimento do mouse
window.addEventListener('mousemove', function(event) {
    mouse.x = event.clientX;
    mouse.y = event.clientY;
});

// Reseta a posição do mouse ao sair da tela
window.addEventListener('mouseout', function() {
    mouse.x = null;
    mouse.y = null;
});

// Ajuste automático do tamanho do canvas
function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    initParticles();
}
window.addEventListener('resize', resizeCanvas);

// Classe que define cada partícula
class Particle {
    constructor(x, y, directionX, directionY, size, color) {
        this.x = x;
        this.y = y;
        this.directionX = directionX;
        this.directionY = directionY;
        this.size = size;
        this.color = color;
    }

    // Método para desenhar a partícula
    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2, false);
        ctx.fillStyle = this.color;
        ctx.fill();
    }

    // Atualiza a posição da partícula
    update() {
        // Colisão com as bordas da tela
        if (this.x > canvas.width || this.x < 0) {
            this.directionX = -this.directionX;
        }
        if (this.y > canvas.height || this.y < 0) {
            this.directionY = -this.directionY;
        }

        // Interação leve com o mouse (Atração magnética suave)
        if (mouse.x != null && mouse.y != null) {
            let dx = mouse.x - this.x;
            let dy = mouse.y - this.y;
            let distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance < mouse.radius) {
                // Força de atração sutil
                this.x += dx * 0.02;
                this.y += dy * 0.02;
            }
        }

        // Movimento padrão
        this.x += this.directionX;
        this.y += this.directionY;

        this.draw();
    }
}

// Inicializa a lista de partículas
function initParticles() {
    particlesArray = [];
    // Ajusta a densidade com base no tamanho da tela
    let numberOfParticles = (canvas.width * canvas.height) / 13000;
    numberOfParticles = Math.min(numberOfParticles, 85); // Limite para garantir performance

    for (let i = 0; i < numberOfParticles; i++) {
        let size = (Math.random() * 2) + 1.2;
        let x = (Math.random() * ((canvas.width - size * 2) - (size * 2)) + size * 2);
        let y = (Math.random() * ((canvas.height - size * 2) - (size * 2)) + size * 2);
        // Velocidades bem lentas e elegantes
        let directionX = (Math.random() * 0.6) - 0.3;
        let directionY = (Math.random() * 0.6) - 0.3;
        
        // Cores alternando entre tons de azul médico e ciano
        let color = Math.random() > 0.5 ? 'rgba(13, 148, 136, 0.25)' : 'rgba(20, 184, 166, 0.2)';

        particlesArray.push(new Particle(x, y, directionX, directionY, size, color));
    }
}

// Conecta as partículas próximas com linhas
function connectParticles() {
    let opacityValue = 1;
    for (let a = 0; a < particlesArray.length; a++) {
        for (let b = a; b < particlesArray.length; b++) {
            let dx = particlesArray[a].x - particlesArray[b].x;
            let dy = particlesArray[a].y - particlesArray[b].y;
            let distance = Math.sqrt(dx * dx + dy * dy);

            // Se as partículas estão próximas, desenha uma linha conectora
            let maxDistance = 140;
            if (distance < maxDistance) {
                opacityValue = 1 - (distance / maxDistance);
                ctx.strokeStyle = `rgba(13, 148, 136, ${opacityValue * 0.08})`;
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.moveTo(particlesArray[a].x, particlesArray[a].y);
                ctx.lineTo(particlesArray[b].x, particlesArray[b].y);
                ctx.stroke();
            }
        }
    }
}

// Loop de animação
function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    for (let i = 0; i < particlesArray.length; i++) {
        particlesArray[i].update();
    }
    connectParticles();
    requestAnimationFrame(animate);
}

// Inicialização inicial do canvas
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
initParticles();
animate();


/* ==========================================================================
   Cronômetro Regressivo (Countdown)
   ========================================================================== */
// Data limite: 11 de Agosto de 2026 às 16h (GMT-03:00 - Fuso Horário de Brasília)
const targetDate = new Date("2026-08-11T16:00:00-03:00").getTime();

const daysEl = document.getElementById('days');
const hoursEl = document.getElementById('hours');
const minutesEl = document.getElementById('minutes');
const secondsEl = document.getElementById('seconds');
const countdownContainer = document.getElementById('countdown-container');

function updateCountdown() {
    const now = new Date().getTime();
    const difference = targetDate - now;

    if (difference <= 0) {
        // Se a data já passou, esconde o countdown ou exibe mensagem
        if (countdownContainer) {
            countdownContainer.innerHTML = `
                <div class="event-started-badge">
                    <span class="pulse-dot"></span>
                    <span class="event-started-text">O EVENTO ESTÁ ACONTECENDO OU JÁ OCORREU!</span>
                </div>
            `;
        }
        clearInterval(countdownInterval);
        return;
    }

    // Cálculos de tempo
    const days = Math.floor(difference / (1000 * 60 * 60 * 24));
    const hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((difference % (1000 * 60)) / 1000);

    // Renderiza na tela com preenchimento de zeros à esquerda (padEnd/padStart)
    daysEl.innerText = days.toString().padStart(2, '0');
    hoursEl.innerText = hours.toString().padStart(2, '0');
    minutesEl.innerText = minutes.toString().padStart(2, '0');
    secondsEl.innerText = seconds.toString().padStart(2, '0');
}

// Atualiza a cada segundo
const countdownInterval = setInterval(updateCountdown, 1000);
updateCountdown(); // Chamada inicial para evitar delay de 1s


/* ==========================================================================
   Integração com o Google Calendar
   ========================================================================== */
const addCalendarBtn = document.getElementById('add-calendar-btn');

if (addCalendarBtn) {
    addCalendarBtn.addEventListener('click', () => {
        const title = encodeURIComponent("Inovação na Área Médica - Rio como Protagonista");
        const details = encodeURIComponent(
            "Evento de inovação médica promovido pela comunidade CRUX.\n\n" +
            "Apoio e Patrocínio:\n" +
            "- CTSADV\n" +
            "- AVIVUS HEALTHTECH\n" +
            "- MARAVALLEY\n\n" +
            "Cronograma:\n" +
            "- 16h às 20h: Painel & Debates sobre Inovação na Medicina\n" +
            "- 19h às 20h: Happy Hour com Chopp liberado!"
        );
        const location = encodeURIComponent("Maravalley - Hub de Inovação - Av. Prof. Pereira Reis, 76 - Santo Cristo, Rio de Janeiro - RJ, 20220-800");
        
        // Data no formato UTC: 11/08/2026 de 16h às 20h (GMT-3 -> UTC: 19h às 23h)
        // Formato: AAAAMMDDTHHMMSSZ
        const dates = "20260811T190000Z/20260811T230000Z";
        
        const googleCalendarUrl = `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${title}&dates=${dates}&details=${details}&location=${location}`;
        
        window.open(googleCalendarUrl, '_blank');
    });
}

/* ==========================================================================
   Accordion / Expandir Mini Currículos
   ========================================================================== */
const bioToggleBtns = document.querySelectorAll('.bio-toggle-btn');

bioToggleBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const bioContent = btn.nextElementSibling;
        const isExpanded = btn.getAttribute('aria-expanded') === 'true';
        
        // Alterna o estado aria-expanded
        btn.setAttribute('aria-expanded', !isExpanded);
        
        // Alterna a classe active no conteúdo
        if (!isExpanded) {
            bioContent.classList.add('active');
            btn.querySelector('span').innerText = 'Fechar mini currículo';
        } else {
            bioContent.classList.remove('active');
            btn.querySelector('span').innerText = 'Ver mini currículo';
        }
    });
});
