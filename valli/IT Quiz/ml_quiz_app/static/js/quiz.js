const form = document.getElementById("answerForm");
const timer = document.getElementById("timer");
let remaining = Number(timer.dataset.seconds);
let submitted = false;

function submitAnswer(answer = "") {
    if (submitted) return;
    submitted = true;
    form.querySelectorAll("button").forEach((button) => {
        button.disabled = true;
    });

    const data = new FormData(form);
    if (answer) data.set("answer", answer);
    fetch(form.action, { method: "POST", body: data })
        .then((response) => response.json())
        .then((payload) => {
            window.location.href = payload.redirect;
        });
}

form.addEventListener("submit", (event) => {
    event.preventDefault();
    submitAnswer(event.submitter?.value || "");
});

const interval = setInterval(() => {
    remaining -= 1;
    timer.textContent = remaining;
    if (remaining <= 5) timer.classList.add("warning");
    if (remaining <= 0) {
        clearInterval(interval);
        submitAnswer("");
    }
}, 1000);
