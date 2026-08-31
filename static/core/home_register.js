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

console.log("HOME REGISTER JS LOADED");