class PureAutoSlider {
    constructor() {
        this.slideTrack = document.getElementById('slideTrack');
        this.slides = document.querySelectorAll('.film-frame');
        
        if (!this.slideTrack) return;
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
        // If film frames exist (e.g. legacy), clone them; SVG strip is already repeated in HTML
        if (!this.slides || this.slides.length === 0) return;
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
            const sprockets = document.querySelectorAll('.film-sprocket-inner');
            const state = document.hidden ? 'paused' : 'running';
            this.slideTrack.style.animationPlayState = state;
            sprockets.forEach(s => s.style.animationPlayState = state);
        });
    }
    
    optimizePerformance() {
        // Add will-change property for better performance
        this.slideTrack.style.willChange = 'transform';
        const sprockets = document.querySelectorAll('.film-sprocket-inner');
        sprockets.forEach(s => s.style.willChange = 'transform');
    }
    
    // Method to pause animation (can be called externally)
    pause() {
        this.slideTrack.style.animationPlayState = 'paused';
        document.querySelectorAll('.film-sprocket-inner').forEach(s => s.style.animationPlayState = 'paused');
    }
    
    // Method to resume animation (can be called externally)
    resume() {
        this.slideTrack.style.animationPlayState = 'running';
        document.querySelectorAll('.film-sprocket-inner').forEach(s => s.style.animationPlayState = 'running');
    }
}

// Initialize slider when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const slider = new PureAutoSlider();
    
    // Make slider globally accessible
    window.autoSlider = slider;
    
    // Add smooth fade-in effect for images
    const images = document.querySelectorAll('.film-frame img');
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
        const images = document.querySelectorAll('.film-frame img');
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
