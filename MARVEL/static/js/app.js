const searchInput = document.querySelector("#live-search");
const searchResults = document.querySelector("#search-results");
const revealCards = document.querySelectorAll(".reveal-card");
const filterButtons = document.querySelectorAll(".filter-chip");
const filterItems = document.querySelectorAll(".filter-grid > div");
const jarvisForm = document.querySelector("#jarvis-form");
const jarvisInput = document.querySelector("#jarvis-input");
const jarvisLog = document.querySelector("#jarvis-log");
const promptButtons = document.querySelectorAll(".prompt-chip");
const soundToggle = document.querySelector("#sound-toggle");

let searchTimer = null;
let audioContext = null;
let oscillator = null;
let gain = null;

function escapeHtml(value) {
    return value.replace(/[&<>"']/g, (char) => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;",
    }[char]));
}

if (searchInput && searchResults) {
    searchInput.addEventListener("input", () => {
        clearTimeout(searchTimer);
        const query = searchInput.value.trim();
        if (!query) {
            searchResults.classList.remove("active");
            searchResults.innerHTML = "";
            return;
        }
        searchTimer = setTimeout(async () => {
            const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
            const results = await response.json();
            searchResults.innerHTML = results.length
                ? results.map((item) => `
                    <a class="search-result" href="${item.url}">
                        <strong>${escapeHtml(item.type)}</strong>
                        <span>${escapeHtml(item.title)}<br><small>${escapeHtml(item.detail || "")}</small></span>
                    </a>
                `).join("")
                : `<div class="search-result"><strong>No Match</strong><span>Try another universe keyword.</span></div>`;
            searchResults.classList.add("active");
        }, 180);
    });

    document.addEventListener("click", (event) => {
        if (!event.target.closest(".search-box")) {
            searchResults.classList.remove("active");
        }
    });
}

if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.12 });
    revealCards.forEach((card) => observer.observe(card));
} else {
    revealCards.forEach((card) => card.classList.add("visible"));
}

filterButtons.forEach((button) => {
    button.addEventListener("click", () => {
        filterButtons.forEach((item) => item.classList.remove("active"));
        button.classList.add("active");
        const filter = button.dataset.filter;
        filterItems.forEach((item) => {
            const category = item.dataset.category || "";
            const visible = filter === "all" || category.includes(filter);
            item.style.display = visible ? "" : "none";
        });
    });
});

function appendJarvisLine(text, type = "system") {
    if (!jarvisLog) return;
    const line = document.createElement("div");
    line.className = `jarvis-line ${type}`;
    line.textContent = text;
    jarvisLog.appendChild(line);
    jarvisLog.scrollTop = jarvisLog.scrollHeight;
}

async function askJarvis(question) {
    appendJarvisLine(`> ${question}`, "user");
    const response = await fetch("/api/jarvis", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
    });
    const payload = await response.json();
    appendJarvisLine(payload.answer, "system");
}

if (jarvisForm && jarvisInput) {
    jarvisForm.addEventListener("submit", (event) => {
        event.preventDefault();
        const question = jarvisInput.value.trim();
        if (!question) return;
        jarvisInput.value = "";
        askJarvis(question);
    });
}

promptButtons.forEach((button) => {
    button.addEventListener("click", () => askJarvis(button.textContent.trim()));
});

if (soundToggle) {
    soundToggle.addEventListener("click", () => {
        if (oscillator) {
            oscillator.stop();
            oscillator.disconnect();
            gain.disconnect();
            oscillator = null;
            gain = null;
            soundToggle.classList.remove("active");
            return;
        }

        audioContext = audioContext || new AudioContext();
        oscillator = audioContext.createOscillator();
        gain = audioContext.createGain();
        oscillator.type = "sawtooth";
        oscillator.frequency.setValueAtTime(72, audioContext.currentTime);
        gain.gain.setValueAtTime(0.018, audioContext.currentTime);
        oscillator.connect(gain);
        gain.connect(audioContext.destination);
        oscillator.start();
        soundToggle.classList.add("active");
    });
}

const canvas = document.querySelector("#particle-canvas");
if (canvas) {
    const context = canvas.getContext("2d");
    const sparks = [];
    const colors = ["#e62429", "#f7c948", "#3ad7ff", "#62f26f", "#b65cff"];

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    function spawnSpark() {
        if (sparks.length > 90) sparks.shift();
        sparks.push({
            x: Math.random() * canvas.width,
            y: canvas.height + 12,
            vx: (Math.random() - 0.5) * 0.55,
            vy: -0.6 - Math.random() * 1.4,
            life: 80 + Math.random() * 90,
            color: colors[Math.floor(Math.random() * colors.length)],
            size: 1 + Math.random() * 2.2,
        });
    }

    function drawSparks() {
        context.clearRect(0, 0, canvas.width, canvas.height);
        if (Math.random() > 0.45) spawnSpark();
        sparks.forEach((spark) => {
            spark.x += spark.vx;
            spark.y += spark.vy;
            spark.life -= 1;
            context.globalAlpha = Math.max(spark.life / 120, 0);
            context.fillStyle = spark.color;
            context.fillRect(spark.x, spark.y, spark.size, spark.size * 3);
        });
        context.globalAlpha = 1;
        for (let index = sparks.length - 1; index >= 0; index -= 1) {
            if (sparks[index].life <= 0) sparks.splice(index, 1);
        }
        requestAnimationFrame(drawSparks);
    }

    resizeCanvas();
    window.addEventListener("resize", resizeCanvas);
    drawSparks();
}
