const eventsGrid = document.querySelector(".events-grid");
const leftArrow = document.querySelector(".left-arrow");
const rightArrow = document.querySelector(".right-arrow");

const card = eventsGrid.querySelector(".reg-comp-card");

const cardWidth = card.offsetWidth;
const gap = parseFloat(getComputedStyle(eventsGrid).gap);

const scrollAmount = (cardWidth + gap) * 3;

rightArrow.addEventListener("click", () => {
    eventsGrid.scrollBy({
        left: scrollAmount,
        behavior: "smooth"
    });
});

leftArrow.addEventListener("click", () => {
    eventsGrid.scrollBy({
        left: -scrollAmount,
        behavior: "smooth"
    });
});

const currentEventId = eventsGrid.dataset.currentEventId;
const currentCityId = eventsGrid.dataset.currentCityId;

const today = new Date();
today.setHours(0, 0, 0, 0);

const eventCards = eventsGrid.querySelectorAll(".reg-comp-card");

eventCards.forEach(card => {
    const eventId = card.dataset.eventId;
    const cityId = card.dataset.cityId;

    const eventDate = new Date(card.dataset.eventDate);
    eventDate.setHours(0, 0, 0, 0);

    // Hide ONLY the exact competition currently displayed above
    if (
        eventId === currentEventId &&
        cityId === currentCityId
    ) {
        card.style.display = "none";
        return;
    }

    // Hide past competitions
    if (eventDate < today) {
        card.style.display = "none";
    }
});