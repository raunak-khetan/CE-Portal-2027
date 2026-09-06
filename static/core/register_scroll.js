const eventsGrid = document.querySelector(".events-grid");
const leftArrow = document.querySelector(".left-arrow");
const rightArrow = document.querySelector(".right-arrow");

rightArrow.addEventListener("click", () => {
    eventsGrid.scrollBy({
        left: eventsGrid.clientWidth,
        behavior: "smooth"
    });
});

leftArrow.addEventListener("click", () => {
    eventsGrid.scrollBy({
        left: -eventsGrid.clientWidth,
        behavior: "smooth"
    });
});