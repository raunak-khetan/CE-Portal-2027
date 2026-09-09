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

        // If the user clicked the Register button/link,
        // let its normal behavior happen.
        if (event.target.closest("a, button")) {
            return;
        }

        // Find the existing registration link inside the card
        const registerLink = card.querySelector("a");

        if (registerLink && registerLink.href) {
            window.location.href = registerLink.href;
        }
    });
});