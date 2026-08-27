document.querySelector(".copy-btn").addEventListener("click", function () {
    const currentUrl = window.location.href; // Get current page URL

    navigator.clipboard.writeText(currentUrl)
        .then(() => {
            // Optional: change text to show feedback
            const textSpan = document.querySelector(".copy-link");
            const originalText = textSpan.textContent;
            textSpan.textContent = "Copied!";
            setTimeout(() => {
                textSpan.textContent = originalText;
            }, 2000);
        })
        .catch(err => {
            console.error("Failed to copy link: ", err);
        });
});
