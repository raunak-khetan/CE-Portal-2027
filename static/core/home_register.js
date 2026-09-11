document.querySelectorAll(".card-actions .register-btn").forEach(button => {
    button.addEventListener("click", function(event) {
        event.preventDefault();

        const link = button.closest(".register-link");

        button.classList.add("clicked");

        setTimeout(() => {
            window.location.href = link.href;
        }, 400);
    });
});

document.querySelectorAll(".comp-card").forEach(card => {
    card.addEventListener("click", function(event) {

        // If Register / Copy Link was clicked directly,
        // let their own handlers run.
        if (event.target.closest("a, button")) {
            return;
        }

        const registerButton = card.querySelector(".card-actions .register-btn");

        if (registerButton) {
            registerButton.click();
        }
    });
});

window.addEventListener("pageshow", function (event) {
    if (event.persisted) {
        window.location.reload();
    }
});