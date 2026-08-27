document.addEventListener('DOMContentLoaded', () => {
	let drop = document.querySelector('.deshboard');
	let desh = document.querySelector('.ul');
	let showBtn = document.querySelector('#drop-btn');
	let display = 1;

	drop.addEventListener('click', (event) => {
		if (display === 1) {
			showBtn.classList.add('rotate');
			desh.style.display = 'block';
			display = 0;
		} else {
			showBtn.classList.remove('rotate');
			desh.style.display = 'none';
			display = 1;
		}
	});

	let currentCity = 'kurukshetra'; // Set the default city as 'Kurukshetra'

	// Fetch the cities data
	fetch('/api/cities/')
		.then((response) => response.json())
		.then((cities) => {
			// Initially render the city list excluding the default current city
			renderCityList(cities, currentCity);

			// Fetch events for Kurukshetra by default on page load
			fetchEventsForCity(currentCity);

			// Set up click event listener for city links after rendering
			document
				.getElementById('ul-1')
				.addEventListener('click', function (event) {
					const link = event.target.closest('.city-link');
					if (link) {
						event.preventDefault();
						const selectedCityName = link.getAttribute('data-city');

						// Update the current city to the clicked city
						currentCity = selectedCityName;

						// Update the city image in the header dynamically
						updateCityImage(selectedCityName);

						// Fetch events for the selected city
						fetchEventsForCity(selectedCityName);

						// Re-render the city list with the newly selected city removed
						renderCityList(cities, currentCity);

						// Redirect to the chosen city page after a short delay
						setTimeout(() => {
							window.location.href = link.href;
						}, 300);
					}
				});
		})
		.catch((error) => {
			console.error('Error fetching city data:', error);
		});

	// Function to render city list except for the current city
	function renderCityList(cities, excludeCity) {
		const cityList = document.getElementById('ul-1');
		cityList.innerHTML = ''; // Clear current city list

		// Filter out the city to exclude and render the rest
		const filteredCities = cities.filter(
			(city) => city.name.toLowerCase() !== excludeCity.toLowerCase()
		);

		filteredCities.forEach((city) => {
			const li = document.createElement('li');
			li.className = slugify(city.name);

			// Creating link element
			const a = document.createElement('a');
			a.href = 'javascript:void(0)';
			a.dataset.city = city.name;
			a.className = 'city-link';

			// Creating image element
			const img = document.createElement('img');
			img.src = `/static/core/asset/${slugify(city.name)}.png`;
			img.alt = city.name;

			// Appending image to link
			a.appendChild(img);

			// Appending link to list item
			li.appendChild(a);

			// Appending list item to the city list
			cityList.appendChild(li);
		});
	}

	// Function to slugify city names
	function slugify(text) {
		return text
			.toString()
			.toLowerCase()
			.replace(/\s+/g, '-') // Replace spaces with -
			.replace(/[^\w-]+/g, '') // Remove all non-word chars
			.replace(/--+/g, '-') // Replace multiple - with single -
			.trim(); // Trim any leading or trailing spaces
	}

	// Function to update the city image in the header dynamically
	function updateCityImage(cityName) {
		const cityImage = document.getElementById('city-img');
		const cityLink = document.querySelector('.city-img-header1 a');

		if (cityImage && cityLink) {
			cityImage.src = `/static/core/asset/${slugify(cityName)}.png`;
			cityImage.alt = cityName;
			cityLink.dataset.city = cityName;
		}
	}

	// second-dropdown
	let drop1 = document.querySelector('#drop1');
	let dash1 = document.querySelector('#ul-1');
	let showBtn1 = document.querySelector('#drop-btn-1');
	let cityimg = document.getElementById('city-img');
	let display1 = 1;

	drop1.addEventListener('click', () => {
		if (display1 === 1) {
			showBtn1.classList.add('rotate');
			dash1.style.display = 'block';
			cityimg.src = `/static/core/asset/${slugify(currentCity)}.png`;
			display1 = 0;
		} else {
			showBtn1.classList.remove('rotate');
			dash1.style.display = 'none';
			display1 = 1;
		}
	});

	const festGrid = document.getElementById('fest-grid');

	function fetchEventsForCity(cityName) {
		fetch(`/get-events/${encodeURIComponent(cityName)}/`)
			.then((response) => {
				if (!response.ok) {
					throw new Error(`HTTP error! status: ${response.status}`);
				}
				return response.json();
			})
			.then((data) => {
				console.log(data);
				festGrid.innerHTML = '';

				data.events.forEach((event) => {
					festGrid.innerHTML += `
              <div class="event-title">${event.name}</div>
              <div class="event-date">${data.time}</div>
            `;
				});

				// Reset dropdown and image to reflect the selected city
				showBtn1.classList.remove('rotate');
				dash1.style.display = 'none';
				display1 = 1;
				cityimg.src = `/static/core/asset/${slugify(cityName)}.png`;
			})
			.catch((error) => console.error('Error fetching events:', error));
	}
});

// Sidebar functions
function showSidebar() {
	const sidebar = document.querySelector('.hamburger');
	sidebar.style.display = 'flex';
}

function hideSidebar() {
	const sidebar = document.querySelector('.hamburger');
	sidebar.style.display = 'none';
}
class PureAutoSlider {
    constructor() {
        this.slideTrack = document.getElementById('slideTrack');
        this.slides = document.querySelectorAll('.slide');
        
        this.init();
    }
    
    init() {
        // Clone slides for seamless infinite loop
        this.createInfiniteLoop();
        
        // Handle visibility change (pause when tab is not visible)
        this.handleVisibilityChange();
        
        // Add performance optimizations
        this.optimizePerformance();
    }
    
    createInfiniteLoop() {
        // Clone all slides twice for seamless infinite scrolling
        const originalSlides = Array.from(this.slides);
        
        // First set of clones
        originalSlides.forEach(slide => {
            const clone = slide.cloneNode(true);
            this.slideTrack.appendChild(clone);
        });
        
        // Second set of clones for extra smoothness
        originalSlides.forEach(slide => {
            const clone = slide.cloneNode(true);
            this.slideTrack.appendChild(clone);
        });
    }
    
    handleVisibilityChange() {
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.slideTrack.style.animationPlayState = 'paused';
            } else {
                this.slideTrack.style.animationPlayState = 'running';
            }
        });
    }
    
    optimizePerformance() {
        // Add will-change property for better performance
        this.slideTrack.style.willChange = 'transform';
        
        // Optimize images loading
        const images = document.querySelectorAll('.slide img');
        images.forEach((img, index) => {
            img.style.animationDelay = `${index * 0.1}s`;
            
            // Add loading optimization
            img.addEventListener('load', () => {
                img.style.opacity = '1';
            });
        });
    }
    
    // Method to pause animation (can be called externally)
    pause() {
        this.slideTrack.style.animationPlayState = 'paused';
    }
    
    // Method to resume animation (can be called externally)
    resume() {
        this.slideTrack.style.animationPlayState = 'running';
    }
}

// Initialize slider when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const slider = new PureAutoSlider();
    
    // Make slider globally accessible
    window.autoSlider = slider;
    
    // Add smooth fade-in effect for images
    const images = document.querySelectorAll('.slide img');
    images.forEach((img, index) => {
        img.style.opacity = '0';
        img.style.transition = 'opacity 0.6s ease';
        
        // Stagger the fade-in effect
        setTimeout(() => {
            img.style.opacity = '1';
        }, index * 100);
    });
    
    // Add intersection observer for performance optimization
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.style.transform = 'scale(1)';
                }
            });
        }, {
            threshold: 0.1
        });
        
        // Observe all images
        const images = document.querySelectorAll('.slide img');
        images.forEach(img => imageObserver.observe(img));
    }
    
    // Add smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const href = link.getAttribute('href');
            if (href && href !== '#') {
                // Smooth scroll to section if it exists
                const targetSection = document.querySelector(href);
                if (targetSection) {
                    targetSection.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
    // Add social media link functionality
    const socialLinks = document.querySelectorAll('.social-link');
    socialLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const href = link.getAttribute('href');
            if (href && href !== '#') {
                // Open social media links in new tab
                window.open(href, '_blank', 'noopener,noreferrer');
            }
        });
    });
});

// Add scroll-based animations for blocks
window.addEventListener('scroll', () => {
    const blocks = document.querySelectorAll('.highway-block, .sponsors-block, .footer-block');
    blocks.forEach(block => {
        const rect = block.getBoundingClientRect();
        const isVisible = rect.top < window.innerHeight && rect.bottom > 0;
        
        if (isVisible) {
            block.style.opacity = '1';
            block.style.transform = 'translateY(0)';
        }
    });
});

// Initialize scroll animations on page load
document.addEventListener('DOMContentLoaded', () => {
    const blocks = document.querySelectorAll('.highway-block, .sponsors-block, .footer-block');
    blocks.forEach(block => {
        block.style.opacity = '0';
        block.style.transform = 'translateY(20px)';
        block.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    });
    
    // Trigger initial animation
    setTimeout(() => {
        blocks.forEach((block, index) => {
            setTimeout(() => {
                block.style.opacity = '1';
                block.style.transform = 'translateY(0)';
            }, index * 200);
        });
    }, 100);
});
