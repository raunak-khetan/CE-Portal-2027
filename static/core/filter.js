document.addEventListener("DOMContentLoaded", () => {

    const filterButtons = document.querySelectorAll(
        ".names-of-competitions-and-filters .filter-button"
    );

    const competitionCards = document.querySelectorAll(".comp-card");

    const clearFilterButton = document.getElementById("clear-filter");

    const allFilterButton = document.querySelector(
        '.names-of-competitions-and-filters [data-filter="all"]'
    );

    let selectedCategories = new Set();
    let selectedDateFilter = null;


    function updateCards() {

        competitionCards.forEach(card => {

            const categoryId = card.dataset.categoryId;
            const eventDate = new Date(card.dataset.eventDate);

            let categoryMatch = true;
            let dateMatch = true;


            // -------------------------
            // CATEGORY FILTER
            // -------------------------

            if (selectedCategories.size > 0) {

                categoryMatch = selectedCategories.has(categoryId);

            }


            // -------------------------
            // DATE FILTER
            // -------------------------

            if (selectedDateFilter === "upcoming") {

                const today = new Date();

                today.setHours(0, 0, 0, 0);
                eventDate.setHours(0, 0, 0, 0);

                dateMatch = eventDate >= today;

            }


            if (selectedDateFilter === "next-month") {

                const today = new Date();

                const nextMonth = today.getMonth() + 1;

                const nextMonthYear =
                    nextMonth === 12
                        ? today.getFullYear() + 1
                        : today.getFullYear();

                const nextMonthIndex =
                    nextMonth === 12
                        ? 0
                        : nextMonth;

                dateMatch =
                    eventDate.getMonth() === nextMonthIndex &&
                    eventDate.getFullYear() === nextMonthYear;

            }


            // -------------------------
            // FINAL RESULT
            // -------------------------

            if (categoryMatch && dateMatch) {
                card.style.display = "block";
            } else {
                card.style.display = "none";
            }

        });
    }


    // -------------------------
    // FILTER BUTTONS
    // -------------------------

    filterButtons.forEach(button => {

        button.addEventListener("click", () => {

            const filter = button.dataset.filter;

            if (!filter) {
                return;
            }


            // -------------------------
            // ALL
            // -------------------------

            if (filter === "all") {
                return;
            }


            // -------------------------
            // UPCOMING
            // -------------------------

            if (filter === "upcoming") {

                selectedDateFilter =
                    selectedDateFilter === "upcoming"
                        ? null
                        : "upcoming";

                if (selectedDateFilter === "upcoming") {
                    button.classList.add("active-filter");
                } else {
                    button.classList.remove("active-filter");
                }

            }


            // -------------------------
            // NEXT MONTH
            // -------------------------

            else if (filter === "next-month") {

                selectedDateFilter =
                    selectedDateFilter === "next-month"
                        ? null
                        : "next-month";

                if (selectedDateFilter === "next-month") {
                    button.classList.add("active-filter");
                } else {
                    button.classList.remove("active-filter");
                }

            }


            // -------------------------
            // CATEGORY
            // -------------------------

            else {

                if (selectedCategories.has(filter)) {

                    selectedCategories.delete(filter);
                    button.classList.remove("active-filter");

                } else {

                    selectedCategories.add(filter);
                    button.classList.add("active-filter");

                }

            }


            // -------------------------
            // HIDE ALL BUTTON
            // -------------------------

            if (
                selectedCategories.size > 0 ||
                selectedDateFilter !== null
            ) {

                allFilterButton.style.display = "none";
                allFilterButton.classList.remove("active-filter");

            } else {

                allFilterButton.style.display = "";
                allFilterButton.classList.add("active-filter");

            }


            updateCards();

        });

    });


    // -------------------------
    // DELETE FILTER
    // -------------------------

    clearFilterButton.addEventListener("click", () => {

        selectedCategories.clear();
        selectedDateFilter = null;


        // Remove active state
        filterButtons.forEach(button => {
            button.classList.remove("active-filter");
        });


        // Show All
        allFilterButton.style.display = "";
        allFilterButton.classList.add("active-filter");


        // Show all cards
        competitionCards.forEach(card => {
            card.style.display = "block";
        });

    });

});