document.addEventListener('DOMContentLoaded', () => {
	// navbar-responsive

	// registeration dropdown

	let drop = document.querySelector('.deshboard');
	let desh = document.querySelector('.ul');
	let showBtn = document.querySelector('#drop-btn');
	let display = 1;
	let head = document.querySelector('#head-img');

	drop.addEventListener('click', () => {
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

	head.addEventListener('click', () => {
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

	// second-dropdown

	let drop1 = document.querySelector('.drop-down');
	let dash1 = document.querySelector('#ul-1');
	let showBtn1 = document.querySelector('#drop-btn-1');
	let cityimg = document.getElementById('city-img');
	let display1 = 1;

	drop1.addEventListener('click', () => {
		if (display1 === 1) {
			showBtn1.classList.add('rotate');
			dash1.style.display = 'block';
			cityimg.src = `/static/core/asset/kurukshetra.png`;
			display1 = 0;
		} else {
			showBtn1.classList.remove('rotate');
			dash1.style.display = 'none';
			display1 = 1;
		}
	});

	// navbar-responsive

	// function showSidebar() {
	// 	const sidebar = document.querySelector('.hamburger');
	// 	sidebar.style.display = 'flex';
	// }

	// function hideSidebar() {
	// 	const sidebar = document.querySelector('.hamburger');
	// 	sidebar.style.display = 'none';
	// }

	const cityLinks = document.querySelectorAll('.city-link');

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

				// Reset dropdown and image
				showBtn1.classList.remove('rotate');
				dash1.style.display = 'none';
				display1 = 1;
				cityimg.src = `/static/core/asset/${cityName}.png`;
			})
			.catch((error) => console.error('Error fetching events:', error));
	}

	// Fetch events for Kurukshetra by default on page load
	fetchEventsForCity('ropar');

	// Set up click event for city links
	cityLinks.forEach((link) => {
		link.addEventListener('click', function (event) {
			event.preventDefault();
			const cityName = this.getAttribute('data-city');
			console.log(cityName);
			fetchEventsForCity(cityName);
		});
	});
});

function showSidebar() {
	const sidebar = document.querySelector('.hamburger');
	sidebar.style.display = 'flex';
}

function hideSidebar() {
	const sidebar = document.querySelector('.hamburger');
	sidebar.style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function () {
	const registrationForm = document.getElementById('registration-form');
	console.log(registrationForm);

	registrationForm.addEventListener('submit', function (e) {
		let isValid = true; // Flag to check overall form validity
		let errorMessages = [];

		const phoneFields = document.querySelectorAll('input[name$="phone_no"]');
		console.log(phoneFields[0].value);

		function validatePhoneNumber(phoneNumber) {
			const phoneRegex = /^\d{10}$/;
			return phoneRegex.test(phoneNumber);
		}

		phoneFields.forEach(function (field) {
			const phoneValue = field.value.trim();
			if (!validatePhoneNumber(phoneValue)) {
				isValid = false;
				errorMessages.push(`Phone number "${phoneValue}" is invalid.`);
			}

			if (!isValid) {
				e.preventDefault(); // Prevent form submission
				const errorContainer = document.createElement('div');

				errorMessages.forEach(function (message) {
					const messageDiv = document.createElement('div');
					messageDiv.textContent = message;
					errorContainer.appendChild(messageDiv);
				});

				// Display all error messages using Toastify
				Toastify({
					node: errorContainer,
					duration: 5000,
					gravity: 'top',
					position: 'right',
					backgroundColor: 'linear-gradient(to right, #ff5f6d, #ffc371)',
					escapeMarkup: false, // Allow line breaks
				}).showToast();
			} else {
				// Set success flag in localStorage
				localStorage.setItem('formSubmitted', 'true');
			}
		});
	});
});
