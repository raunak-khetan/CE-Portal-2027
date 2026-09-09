document.addEventListener("DOMContentLoaded", () => {

    // =========================
    // FILTER ELEMENTS
    // =========================

    const filterButtons = document.querySelectorAll(
        ".names-of-competitions-and-filters .filter-button, .mobile-filter-option"
    );

    const competitionCards =
        document.querySelectorAll(".comp-card");

    const clearFilterButton =
        document.getElementById("clear-filter");

    const allFilterButton =
        document.querySelector(
            '.names-of-competitions-and-filters [data-filter="all"]'
        );


    // =========================
    // SEARCH
    // =========================

    const searchInput =
        document.querySelector(".mobile-search input");

    const recommendationBox =
        document.querySelector(".search-recommendations");


    // =========================
    // MOBILE FILTER
    // =========================

    const mobileFilterButton =
        document.querySelector(".mobile-filter-button");

    const allFiltersButton =
        document.querySelector(".all-filter-button");

    const mobileFilterPanel =
        document.getElementById("mobileFilterPanel");

    const mobileFilterClose =
        document.getElementById("mobileFilterClose");

    const mobileFilterClear =
        document.getElementById("mobileFilterClear");

    const mobileFilterOptions =
        document.querySelectorAll(".mobile-filter-option");


    // =========================
    // CITY DROPDOWN
    // =========================

    const cityButton =
        document.getElementById(
            "competitionsCityButton"
        );

    const cityDropdownMenu =
        document.getElementById(
            "cityDropdownMenu"
        );

    const cityDropdown =
        document.querySelector(
            ".city-dropdown"
        );

    const citySearchInput =
        document.getElementById(
            "citySearchInput"
        );

    const cityOptions =
        document.querySelectorAll(
            ".city-option"
        );

    const locationText =
        document.querySelector(
            ".select-location-text"
        );


    // =========================
    // CATEGORY NAMES
    // =========================

    const categoryNames = {};

    filterButtons.forEach(button => {

        const categoryId =
            button.dataset.filter;

        if (
            categoryId &&
            categoryId !== "all" &&
            categoryId !== "upcoming" &&
            categoryId !== "next-month"
        ) {

            categoryNames[categoryId] =
                button.textContent.trim();

        }

    });


    // =========================
    // SELECTED FILTERS
    // =========================

    let selectedCategories = new Set();

    let selectedDateFilter = null;

    let searchText = "";

    let selectedCityId = null;


    // =========================
    // UPDATE FILTER BUTTON UI
    // =========================

    function updateFilterButtonStates() {

        // =========================
        // UPDATE ALL FILTER BUTTONS
        // =========================

        filterButtons.forEach(button => {

            const filter = button.dataset.filter;

            if (!filter) {
                return;
            }


            // =========================
            // DATE FILTERS
            // =========================

            if (
                filter === "upcoming" ||
                filter === "next-month"
            ) {

                button.classList.toggle(
                    "active-filter",
                    selectedDateFilter === filter
                );

            }


            // =========================
            // CATEGORY FILTERS
            // =========================

            else if (filter !== "all") {

                const isSelected = selectedCategories.has(filter);

                button.classList.toggle(
                    "active-filter",
                    isSelected
                );

                // On tablet, show a category in the filter bar
                // if it has been selected from All Filters.
                if (button.classList.contains("category-filter")) {

                    button.classList.toggle(
                        "selected-visible-filter",
                        isSelected
                    );

                }

            }

        });


        // =========================
        // ALL BUTTON
        // =========================

        if (allFilterButton) {

            const hasOtherFilters =
                selectedCategories.size > 0 ||
                selectedDateFilter !== null;


            if (hasOtherFilters) {

                allFilterButton.style.display = "none";

                allFilterButton.classList.remove(
                    "active-filter"
                );

            } else {

                allFilterButton.style.display = "";

                allFilterButton.classList.add(
                    "active-filter"
                );

            }

        }

    }


    // =========================
    // UPDATE CARDS
    // =========================

    function updateCards() {

        competitionCards.forEach(card => {

            const categoryId =
                card.dataset.categoryId;

            const eventDate =
                new Date(card.dataset.eventDate);

            let categoryMatch = true;

            let dateMatch = true;

            let searchMatch = true;

            let cityMatch = true;


            // =========================
            // CITY FILTER
            // =========================

            if (selectedCityId !== null) {

                cityMatch =
                    card.dataset.cityId === selectedCityId;

            }


            // =========================
            // CATEGORY FILTER
            // =========================

            if (selectedCategories.size > 0) {

                categoryMatch =
                    selectedCategories.has(categoryId);

            }


            // =========================
            // UPCOMING
            // =========================

            if (
                selectedDateFilter === "upcoming"
            ) {

                const today =
                    new Date();

                today.setHours(
                    0,
                    0,
                    0,
                    0
                );

                eventDate.setHours(
                    0,
                    0,
                    0,
                    0
                );

                dateMatch =
                    eventDate >= today;

            }


            // =========================
            // NEXT MONTH
            // =========================

            if (
                selectedDateFilter === "next-month"
            ) {

                const today =
                    new Date();

                const nextMonth =
                    today.getMonth() + 1;

                const nextMonthYear =
                    nextMonth === 12
                        ? today.getFullYear() + 1
                        : today.getFullYear();

                const nextMonthIndex =
                    nextMonth === 12
                        ? 0
                        : nextMonth;

                dateMatch =
                    eventDate.getMonth() ===
                        nextMonthIndex &&
                    eventDate.getFullYear() ===
                        nextMonthYear;

            }


            // =========================
            // SEARCH
            // =========================

            if (searchText !== "") {

                const titleElement =
                    card.querySelector(".card-title");

                const title =
                    titleElement
                        ? titleElement.textContent
                            .trim()
                            .toLowerCase()
                        : "";

                const categoryName =
                    categoryNames[categoryId]
                        ? categoryNames[categoryId]
                            .toLowerCase()
                        : "";

                const titleMatches =
                    title.includes(searchText);

                const categoryMatches =
                    categoryName.includes(searchText);

                searchMatch =
                    titleMatches ||
                    categoryMatches;

            }


            // =========================
            // FINAL RESULT
            // =========================

            if (
                cityMatch &&
                categoryMatch &&
                dateMatch &&
                searchMatch
            ) {

                card.style.display =
                    "block";

            } else {

                card.style.display =
                    "none";

            }

        });

    }


    // =========================
    // SEARCH + RECOMMENDATIONS
    // =========================

    if (searchInput) {

        searchInput.addEventListener(
            "input",
            () => {

                searchText =
                    searchInput.value
                        .trim()
                        .toLowerCase();


                // Update cards
                updateCards();


                // No recommendation box
                if (!recommendationBox) {
                    return;
                }


                // Clear old recommendations
                recommendationBox.innerHTML = "";


                // Nothing typed
                if (searchText === "") {

                    recommendationBox.classList.remove(
                        "show"
                    );

                    return;

                }


                const recommendations = [];


                // =========================
                // FIND RECOMMENDATIONS
                // =========================

                competitionCards.forEach(card => {

                    const titleElement =
                        card.querySelector(
                            ".card-title"
                        );

                    if (!titleElement) {
                        return;
                    }

                    const title =
                        titleElement
                            .textContent
                            .trim();

                    const categoryId =
                        card.dataset.categoryId;

                    const categoryName =
                        categoryNames[categoryId] || "";

                    const titleMatches =
                        title
                            .toLowerCase()
                            .includes(searchText);

                    const categoryMatches =
                        categoryName
                            .toLowerCase()
                            .includes(searchText);

                    if (
                        (titleMatches ||
                            categoryMatches) &&
                        !recommendations.some(
                            item =>
                                item.title === title
                        )
                    ) {

                        recommendations.push({
                            title: title,
                            category: categoryName
                        });

                    }

                });


                // =========================
                // SHOW RECOMMENDATIONS
                // =========================

                recommendations
                    .slice(0, 5)
                    .forEach(item => {

                        const button =
                            document.createElement(
                                "button"
                            );

                        button.type =
                            "button";

                        button.className =
                            "search-recommendation";

                        button.innerHTML = `
                            <span>${item.title}</span>
                            <small>${item.category}</small>
                        `;

                        button.addEventListener(
                            "click",
                            () => {

                                searchInput.value =
                                    item.title;

                                searchText =
                                    item.title
                                        .toLowerCase();

                                recommendationBox
                                    .classList
                                    .remove("show");

                                updateCards();

                            }
                        );

                        recommendationBox
                            .appendChild(button);

                    });


                if (
                    recommendations.length > 0
                ) {

                    recommendationBox
                        .classList
                        .add("show");

                } else {

                    recommendationBox
                        .classList
                        .remove("show");

                }

            }
        );


        // =========================
        // SEARCH CLICK OUTSIDE
        // =========================

        document.addEventListener(
            "click",
            event => {

                if (
                    !event.target.closest(
                        ".mobile-search-wrapper"
                    )
                ) {

                    if (recommendationBox) {

                        recommendationBox
                            .classList
                            .remove("show");

                    }

                }

            }
        );

    }


    // =========================
    // FILTER BUTTONS
    // =========================

    filterButtons.forEach(button => {

        button.addEventListener(
            "click",
            event => {

                const filter =
                    button.dataset.filter;


                if (!filter) {
                    return;
                }


                // =========================
                // ALL
                // =========================

                if (filter === "all") {

                    selectedCategories.clear();

                    selectedDateFilter = null;

                }


                // =========================
                // UPCOMING
                // =========================

                else if (
                    filter === "upcoming"
                ) {

                    if (
                        selectedDateFilter ===
                        "upcoming"
                    ) {

                        selectedDateFilter =
                            null;

                    } else {

                        selectedDateFilter =
                            "upcoming";

                    }

                }


                // =========================
                // NEXT MONTH
                // =========================

                else if (
                    filter === "next-month"
                ) {

                    if (
                        selectedDateFilter ===
                        "next-month"
                    ) {

                        selectedDateFilter =
                            null;

                    } else {

                        selectedDateFilter =
                            "next-month";

                    }

                }


                // =========================
                // CATEGORY
                // =========================

                else {

                    if (
                        selectedCategories.has(
                            filter
                        )
                    ) {

                        selectedCategories.delete(
                            filter
                        );

                    } else {

                        selectedCategories.add(
                            filter
                        );

                    }

                }


                // =========================
                // UPDATE BUTTON STATES
                // =========================

                updateFilterButtonStates();


                // =========================
                // UPDATE CARDS
                // =========================

                updateCards();


                // =========================
                // CLOSE MOBILE FILTER
                // AFTER SELECTING FILTER
                // =========================

            }
        );

    });


    // =========================
    // ALL FILTERS BUTTON
    // =========================

    if (allFiltersButton && mobileFilterPanel) {

        allFiltersButton.addEventListener(
            "click",
            event => {

                event.preventDefault();
                event.stopPropagation();


                // =========================
                // CLOSE CITY DROPDOWN
                // =========================

                if (cityDropdownMenu) {

                    cityDropdownMenu
                        .classList
                        .remove("show");

                }

                if (cityButton) {

                    cityButton.setAttribute(
                        "aria-expanded",
                        "false"
                    );

                }


                // =========================
                // POSITION FILTER PANEL
                // =========================

                const isOpening =
                    !mobileFilterPanel.classList.contains("show");


                if (isOpening) {

                    const rect =
                        allFiltersButton.getBoundingClientRect();


                    mobileFilterPanel.style.top =
                        `${rect.bottom + 8}px`;


                    mobileFilterPanel.style.right =
                        `${window.innerWidth - rect.right}px`;

                }


                // =========================
                // TOGGLE FILTER PANEL
                // =========================

                mobileFilterPanel
                    .classList
                    .toggle("show");

            }
        );

    }


    // =========================
    // DESKTOP CLEAR FILTER
    // =========================

    if (clearFilterButton) {

        clearFilterButton.addEventListener(
            "click",
            () => {

                selectedCategories.clear();

                selectedDateFilter = null;


                updateFilterButtonStates();

                updateCards();

            }
        );

    }


    // =========================
    // MOBILE FILTER BUTTON
    // =========================

    if (mobileFilterButton && mobileFilterPanel){

        mobileFilterButton.addEventListener(
            "click",
            event => {

                event.stopPropagation();


                // =========================
                // CLOSE CITY DROPDOWN
                // =========================

                if (cityDropdownMenu) {

                    cityDropdownMenu
                        .classList
                        .remove("show");

                }

                if (cityButton) {

                    cityButton.setAttribute(
                        "aria-expanded",
                        "false"
                    );

                }


                // =========================
                // POSITION MOBILE FILTER
                // =========================

                const isOpening =
                    !mobileFilterPanel.classList.contains("show");

                if (isOpening) {

                    const rect =
                        mobileFilterButton.getBoundingClientRect();

                    mobileFilterPanel.style.top =
                        `${rect.bottom + 8}px`;

                    mobileFilterPanel.style.right =
                        `${window.innerWidth - rect.right}px`;
                }


                // =========================
                // TOGGLE MOBILE FILTER
                // =========================

                mobileFilterPanel
                    .classList
                    .toggle("show");

            }
        );

    }


    // =========================
    // MOBILE FILTER CLOSE BUTTON
    // =========================

    if (
        mobileFilterClose &&
        mobileFilterPanel
    ) {

        mobileFilterClose.addEventListener(
            "click",
            event => {

                event.stopPropagation();


                mobileFilterPanel
                    .classList
                    .remove("show");

            }
        );

    }


    // =========================
    // MOBILE CLEAR FILTER
    // =========================

    if (mobileFilterClear) {

        mobileFilterClear.addEventListener(
            "click",
            event => {

                event.stopPropagation();


                selectedCategories.clear();

                selectedDateFilter = null;


                updateFilterButtonStates();

                updateCards();


                // =========================
                // CLOSE FILTER PANEL
                // =========================

                if (mobileFilterPanel) {

                    mobileFilterPanel
                        .classList
                        .remove("show");

                }

            }
        );

    }


    // =========================
    // CLOSE MOBILE FILTER
    // WHEN CLICKING OUTSIDE
    // =========================

    document.addEventListener(
        "click",
        event => {

            if (!mobileFilterPanel) {
                return;
            }


            const clickedInsideFilter =
                mobileFilterPanel.contains(
                    event.target
                );


            const clickedFilterButton =
                mobileFilterButton &&
                mobileFilterButton.contains(
                    event.target
                );


            const clickedAllFiltersButton =
                allFiltersButton &&
                allFiltersButton.contains(
                    event.target
                );


            if (
                !clickedInsideFilter &&
                !clickedFilterButton &&
                !clickedAllFiltersButton
            ) {

                mobileFilterPanel
                    .classList
                    .remove("show");

            }

        }
    );


    // =========================
    // CITY DROPDOWN
    // =========================

    if (
        cityButton &&
        cityDropdownMenu &&
        cityDropdown
    ) {

        // =========================
        // OPEN / CLOSE CITY DROPDOWN
        // =========================

        const locationTrigger =
            document.querySelector(
                ".city-select"
            );


        if (locationTrigger) {

            locationTrigger.addEventListener(
                "click",
                event => {

                    // =========================
                    // CLOSE MOBILE FILTER
                    // =========================

                    if (mobileFilterPanel) {

                        mobileFilterPanel
                            .classList
                            .remove("show");

                    }


                    // =========================
                    // IGNORE CLICKS INSIDE DROPDOWN
                    // =========================

                    if (
                        cityDropdownMenu &&
                        cityDropdownMenu.contains(
                            event.target
                        )
                    ) {

                        return;

                    }


                    event.stopPropagation();


                    // =========================
                    // TOGGLE CITY DROPDOWN
                    // =========================

                    const isOpen =
                        cityDropdownMenu
                            .classList
                            .toggle("show");


                    cityButton.setAttribute(
                        "aria-expanded",
                        isOpen
                    );


                    if (
                        isOpen &&
                        citySearchInput
                    ) {

                        setTimeout(
                            () => {

                                citySearchInput
                                    .focus();

                            },
                            50
                        );

                    }

                }
            );

        }


        // =========================
        // SEARCH CITIES
        // =========================

        if (citySearchInput) {

            citySearchInput.addEventListener(
                "input",
                () => {

                    const searchValue =
                        citySearchInput.value
                            .trim()
                            .toLowerCase();


                    cityOptions.forEach(
                        option => {

                            const cityName =
                                (
                                    option.dataset.cityName ||
                                    ""
                                ).toLowerCase();


                            const stateName =
                                (
                                    option.dataset.state ||
                                    ""
                                ).toLowerCase();


                            const cityMatches =
                                cityName.includes(
                                    searchValue
                                );


                            const stateMatches =
                                stateName.includes(
                                    searchValue
                                );


                            if (
                                cityMatches ||
                                stateMatches
                            ) {

                                option.style.display =
                                    "block";

                            } else {

                                option.style.display =
                                    "none";

                            }

                        }
                    );

                }
            );

        }


        // =========================
        // SELECT CITY
        // =========================

        cityOptions.forEach(
            option => {

                option.addEventListener(
                    "click",
                    event => {

                        event.stopPropagation();


                        const cityId =
                            option.dataset.cityId;


                        const cityName =
                            option.dataset.cityName;


                        // =========================
                        // ALL
                        // =========================

                        if (
                            cityId === "all"
                        ) {

                            selectedCityId =
                                null;


                            if (locationText) {

                                locationText.textContent =
                                    "Choose a location";

                            }

                        }


                        // =========================
                        // SPECIFIC CITY
                        // =========================

                        else {

                            selectedCityId =
                                cityId;


                            if (locationText) {

                                locationText.textContent =
                                    cityName;

                            }

                        }


                        // Apply city filter
                        // while preserving
                        // category/date/search
                        updateCards();


                        // =========================
                        // CLOSE DROPDOWN
                        // =========================

                        cityDropdownMenu
                            .classList
                            .remove("show");


                        cityButton.setAttribute(
                            "aria-expanded",
                            "false"
                        );


                        // =========================
                        // CLEAR CITY SEARCH
                        // =========================

                        if (citySearchInput) {

                            citySearchInput.value =
                                "";


                            cityOptions.forEach(
                                cityOption => {

                                    cityOption.style.display =
                                        "block";

                                }
                            );

                        }

                    }
                );

            }
        );


        // =========================
        // CITY CLICK OUTSIDE
        // =========================

        document.addEventListener(
            "click",
            event => {

                if (
                    !cityDropdown.contains(
                        event.target
                    )
                ) {

                    cityDropdownMenu
                        .classList
                        .remove("show");


                    cityButton.setAttribute(
                        "aria-expanded",
                        "false"
                    );

                }

            }
        );

    }


    // =========================
    // INITIAL STATE
    // =========================

    updateFilterButtonStates();

    updateCards();

});