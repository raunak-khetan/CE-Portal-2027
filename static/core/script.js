// raunak start
//home.html script
console.log("🔥 About Section JS Loaded");

document.addEventListener("DOMContentLoaded", function () {
  // Hero slider
  const imageWrap = document.querySelector(".image-1");
  const prevBtn = document.querySelector(".image-nav .slidebtn:first-of-type");
  const nextBtn = document.querySelector(".image-nav .slidebtn:last-of-type");
  const dotsWrap = document.querySelector(".image-nav .slide-dots");

  if (imageWrap && prevBtn && nextBtn && dotsWrap) {
    const imgsAttr = imageWrap.getAttribute("data-images");
    let sources = [];
    try {
      sources = JSON.parse(imgsAttr || "[]");
    } catch {}
    if (!Array.isArray(sources) || sources.length === 0) return;

    let index = Number(imageWrap.getAttribute("data-start-index") || 0);
    index = isNaN(index) ? 0 : Math.max(0, Math.min(index, sources.length - 1));

    // Build track/slides
    const track = document.createElement("div");
    track.className = "slider-track";
    track.style.transform = `translateX(-${index * 100}%)`;
    sources.forEach((src) => {
      const slide = document.createElement("div");
      slide.className = "slider-slide";
      const img = document.createElement("img");
      img.src = src;
      img.alt = "";
      slide.appendChild(img);
      track.appendChild(slide);
    });
    // Clear existing and inject
    imageWrap.innerHTML = "";
    imageWrap.appendChild(track);

    function renderDots() {
      dotsWrap.innerHTML = sources
        .map(
          (_, i) =>
            `<span class="slide-dot${i === index ? " is-active" : ""}"></span>`
        )
        .join("");
    }
    function show(i) {
      index = (i + sources.length) % sources.length;
      track.style.transform = `translateX(-${index * 100}%)`;
      renderDots();
    }
    function next() {
      show(index + 1);
    }
    function prev() {
      show(index - 1);
    }

    prevBtn.addEventListener("click", prev);
    nextBtn.addEventListener("click", next);
    dotsWrap.addEventListener("click", (e) => {
      const all = Array.from(dotsWrap.querySelectorAll(".slide-dot"));
      const idx = all.indexOf(e.target.closest(".slide-dot"));
      if (idx >= 0) show(idx);
    });

    // init
    renderDots();
    show(index);
  }

  const button = document.getElementById("competitionsCityButton");
  const list = document.getElementById("competitionsCityList");
  const sections = document.querySelectorAll(".city-competitions");
  const allSection = document.getElementById("city-all");

  function showList(show) {
    if (!list) return;
    list.hidden = !show;
    button.setAttribute("aria-expanded", String(show));
  }

  function updateVisibleCity(value) {
    const targetId = value || "city-all";
  
    sections.forEach((sec) => {
      if (sec.id === targetId) {
        sec.classList.remove("is-hidden");
      } else {
        sec.classList.add("is-hidden");
      }
    });
  
    if (allSection && targetId !== "city-all") {
      allSection.classList.add("is-hidden");
    } else if (allSection && targetId === "city-all") {
      allSection.classList.remove("is-hidden");
    }
  }
  

  if (button && list) {
    button.addEventListener("click", () => showList(list.hidden));
    list.addEventListener("click", (e) => {
      const li = e.target.closest('li[role="option"]');
      if (!li) return;
      list
        .querySelectorAll("li")
        .forEach((el) => el.classList.remove("is-active"));
      li.classList.add("is-active");
      const value = li.getAttribute("data-value");
      button.textContent = li.textContent + " ▾";
      showList(false);
      updateVisibleCity(value);
    });
    // Initialize
    updateVisibleCity("city-all");
  }
});

//register.html script
(function () {
  const membersContainer = document.getElementById("members-container");
  const addBtn = document.getElementById("add-member");
  const teamSizeInput = document.getElementById("team-size");

  console.log("Register script running. Elements found:", {
    membersContainer: !!membersContainer,
    addBtn: !!addBtn,
    teamSizeInput: !!teamSizeInput
  });

  // Only run on register page where these elements exist (team events only)
  if (!membersContainer || !addBtn || !teamSizeInput) {
    console.log("Register script exiting - missing required elements (not a team event or elements not found)");
    return;
  }

  // Detect Django formset management inputs without needing a prefix from template
  const totalFormsInput = document.querySelector('input[name$="-TOTAL_FORMS"]');
  const maxFormsInput = document.querySelector('input[name$="-MAX_NUM_FORMS"]');
  const minFormsInput = document.querySelector('input[name$="-MIN_NUM_FORMS"]');

  const maxParticipants = Number(maxFormsInput?.value || 100);
  const minParticipants = Number(minFormsInput?.value || 0);

  function currentMemberCount() {
    // Head counts as 1; extra members are number of visible member cards
    return 1 + membersContainer.querySelectorAll(".member-card").length;
  }

  function updateTeamSize() {
    teamSizeInput.value = currentMemberCount();
    // Disable add button if we reached max
    addBtn.disabled = currentMemberCount() >= maxParticipants;
  }

  function renumberMembers() {
    const cards = membersContainer.querySelectorAll(".member-card");
    cards.forEach((card, idx) => {
      const num = idx + 2; // Member 2..N
      const title = card.querySelector("h3");
      if (title) title.textContent = `Member ${num}`;
    });
  }

  function addMember() {
    if (currentMemberCount() >= maxParticipants) return;
    const tmpl = document.getElementById("empty-member-template").innerHTML;
    const formIndex = Number(totalFormsInput?.value || 0);
    const html = tmpl
      .replaceAll("__NUM__", formIndex + 2)
      .replaceAll("__prefix__", String(formIndex));

    const wrapper = document.createElement("div");
    wrapper.innerHTML = html.trim();
    const card = wrapper.firstElementChild;

    // Update field names and IDs to use the correct form index
    card.querySelectorAll("[name]").forEach((el) => {
      if (el.name.includes("-__prefix__-")) {
        el.name = el.name.replace("-__prefix__-", `-${formIndex}-`);
      }
    });
    card.querySelectorAll("[id]").forEach((el) => {
      if (el.id.includes("__prefix__")) {
        el.id = el.id.replace("__prefix__", String(formIndex));
      }
    });

    card.addEventListener("click", function (e) {
      if (e.target && e.target.matches("[data-remove]")) {
        card.remove();
        // We do not decrement TOTAL_FORMS to keep indexes unique; it's acceptable for model formsets
        renumberMembers();
        updateTeamSize();
      }
    });

    membersContainer.appendChild(card);
    if (totalFormsInput) totalFormsInput.value = String(formIndex + 1);
    renumberMembers();
    updateTeamSize();
  }

  addBtn.addEventListener("click", addMember);
  membersContainer.addEventListener("click", function (e) {
    if (e.target && e.target.matches("[data-remove]")) {
      const card = e.target.closest(".member-card");
      if (card) {
        card.remove();
        renumberMembers();
        updateTeamSize();
      }
    }
  });

  updateTeamSize();
})();
// raunak end

//ashsih start
document.querySelector(".hamburger").addEventListener("click", function () {
  const menu = document.getElementById("nav-menu");
  menu.classList.toggle("show");
});

document.addEventListener("DOMContentLoaded", () => {
  const counters = document.querySelectorAll(".counter");

  counters.forEach((counter) => {
    const updateCount = () => {
      const target = +counter.getAttribute("data-target");
      const current = +counter.innerText;
      const increment = Math.ceil(target / 100); // speed of counting

      if (current < target) {
        counter.innerText = current + increment;
        setTimeout(updateCount, 30); // adjust for speed
      } else {
        counter.innerText = target;
      }
    };

    updateCount();
  });
});


let slideIndex = 0;
const slides = document.querySelectorAll(".about-slide");

const dots = document.querySelectorAll(".dot");
const totalSlides = slides.length;
const prevBtn = document.querySelector(".about-prev");
const nextBtn = document.querySelector(".about-next");

function showSlide(index) {
  slideIndex = index;

  slides.forEach((slide, i) => {
    slide.classList.toggle("active", i === index);
  });

  dots.forEach((dot, i) => {
    dot.classList.toggle("active", i === index);
  });
}

function nextSlide() {
  slideIndex = (slideIndex + 1) % totalSlides;
  showSlide(slideIndex);
}

function prevSlide() {
  slideIndex = (slideIndex - 1 + totalSlides) % totalSlides;
  showSlide(slideIndex);
}

// Button click listeners
nextBtn.addEventListener("click", () => {
  nextSlide();
  resetAutoSlide();
});

prevBtn.addEventListener("click", () => {
  prevSlide();
  resetAutoSlide();
});

// Dot click listeners
dots.forEach((dot) => {
  dot.addEventListener("click", () => {
    const index = parseInt(dot.getAttribute("data-index"));
    showSlide(index);
    resetAutoSlide();
  });
});

// Auto slide with reset on manual interaction
let autoSlideInterval = setInterval(nextSlide, 4000);

function resetAutoSlide() {
  clearInterval(autoSlideInterval);
  autoSlideInterval = setInterval(nextSlide, 4000);
}

// Initialize
showSlide(slideIndex);

//ashish start upcoming events

 document.addEventListener('DOMContentLoaded', () => {
    const carousel = document.querySelector('.carousel');
    const leftArrow = document.querySelector('.nav-btn.left');
    const rightArrow = document.querySelector('.nav-btn.right');
    const pagination = document.querySelector('.pagination');
    const cards = document.querySelectorAll('.competition-card');

    if (!carousel || cards.length === 0) return;

    const cardStyle = window.getComputedStyle(cards[0]);
    const gap = parseInt(cardStyle.marginRight || 20);
    const cardWidth = cards[0].offsetWidth + gap;
    const carouselWidth = carousel.clientWidth;

    const visibleCards = Math.floor(carouselWidth / cardWidth);
    const totalPages = Math.ceil(cards.length / visibleCards);
    let currentPage = 0;

    // Clear any previous dots (important if this re-runs)
    pagination.innerHTML = '';

    // Generate pagination dots
    for (let i = 0; i < totalPages; i++) {
      const dot = document.createElement('span');
      dot.classList.add('dot');
      if (i === 0) dot.classList.add('active');
      dot.addEventListener('click', () => {
        currentPage = i;
        scrollToPage();
      });
      pagination.appendChild(dot);
    }

    const updateDots = () => {
      document.querySelectorAll('.dot').forEach((dot, index) => {
        dot.classList.toggle('active', index === currentPage);
      });
    };

    function scrollToPage() {
      carousel.scrollTo({
        left: currentPage * cardWidth * visibleCards,
        behavior: 'smooth'
      });
      updateDots();
    }

    leftArrow.addEventListener('click', () => {
      if (currentPage > 0) {
        currentPage--;
        scrollToPage();
      }
    });

    rightArrow.addEventListener('click', () => {
      if (currentPage < totalPages - 1) {
        currentPage++;
        scrollToPage();
      }
    });
  });
//ashish end upcoming events
