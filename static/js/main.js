/* ═══════════════════════════════════════════════════════════
   ADITYA PORTFOLIO – Main JavaScript + Vue.js
   ═══════════════════════════════════════════════════════════ */

// ─── Initialize AOS Animations ─────────────────────────────
document.addEventListener('DOMContentLoaded', function () {

    // AOS (Animate On Scroll)
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-out-cubic',
            once: true,
            offset: 80,
            delay: 50
        });
    }

    // ─── Navbar Scroll Effect ──────────────────────────────
    const navbar = document.getElementById('mainNavbar');
    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // ─── Smooth Scrolling for Nav Links ────────────────────
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const offset = 80;
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - offset;
                window.scrollTo({ top: targetPosition, behavior: 'smooth' });

                // Close mobile menu
                const navCollapse = document.getElementById('navbarNav');
                if (navCollapse && navCollapse.classList.contains('show')) {
                    const bsCollapse = bootstrap.Collapse.getInstance(navCollapse);
                    if (bsCollapse) bsCollapse.hide();
                }
            }
        });
    });

    // ─── Active Nav Link on Scroll ─────────────────────────
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');

    function updateActiveNav() {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 120;
            if (window.scrollY >= sectionTop) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + current) {
                link.classList.add('active');
            }
        });
    }

    window.addEventListener('scroll', updateActiveNav);
    updateActiveNav();

    // ─── Skill Progress Bar Animation ──────────────────────
    const progressBars = document.querySelectorAll('.progress-bar[data-target]');

    const animateProgressBars = () => {
        progressBars.forEach(bar => {
            const rect = bar.getBoundingClientRect();
            if (rect.top < window.innerHeight - 50 && !bar.dataset.animated) {
                bar.dataset.animated = 'true';
                const target = bar.getAttribute('data-target');
                setTimeout(() => {
                    bar.style.width = target + '%';
                }, 200);
            }
        });
    };

    window.addEventListener('scroll', animateProgressBars);
    animateProgressBars(); // Run once on load

    // ─── Contact Form Validation ───────────────────────────
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function (e) {
            const name = document.getElementById('name').value.trim();
            const email = document.getElementById('email').value.trim();
            const message = document.getElementById('message').value.trim();

            if (!name || !email || !message) {
                e.preventDefault();
                showAlert('Please fill in all fields.', 'warning');
                return;
            }

            // Email regex validation
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                e.preventDefault();
                showAlert('Please enter a valid email address.', 'warning');
                return;
            }
        });
    }

    // ─── Auto-dismiss Flash Messages ───────────────────────
    setTimeout(() => {
        document.querySelectorAll('.flash-container .alert').forEach(alert => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        });
    }, 5000);

    // ─── Typing Effect for Hero (optional enhancement) ─────
    const heroTitle = document.querySelector('.hero-section h1');
    if (heroTitle) {
        heroTitle.style.opacity = '0';
        heroTitle.style.transform = 'translateY(20px)';
        setTimeout(() => {
            heroTitle.style.transition = 'all 0.8s ease';
            heroTitle.style.opacity = '1';
            heroTitle.style.transform = 'translateY(0)';
        }, 300);
    }

});


// ─── Vue.js App for Dynamic Project Filtering ──────────────
// This creates an interactive project filter if Vue is available
if (typeof Vue !== 'undefined') {
    const projectsAppEl = document.getElementById('projectsApp');
    if (projectsAppEl) {
        // Vue app can be extended for filtering, search, etc.
        // Currently the projects are rendered server-side via Jinja2
        // Vue is available for future interactive enhancements
    }
}


// ─── Utility: Show Alert ───────────────────────────────────
function showAlert(message, type = 'info') {
    const container = document.querySelector('.flash-container') || createFlashContainer();
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show shadow-lg`;
    alert.setAttribute('role', 'alert');
    alert.innerHTML = `
        <i class="bi bi-${type === 'success' ? 'check-circle' : type === 'danger' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    container.appendChild(alert);

    setTimeout(() => {
        const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
        if (bsAlert) bsAlert.close();
    }, 4000);
}

function createFlashContainer() {
    const container = document.createElement('div');
    container.className = 'flash-container';
    container.style.cssText = 'position:fixed;top:80px;right:20px;z-index:9999;width:350px;';
    document.body.appendChild(container);
    return container;
}


// ─── Counter Animation (for hero stats) ────────────────────
function animateCounter(el, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);
    const timer = setInterval(() => {
        start += increment;
        if (start >= target) {
            el.textContent = target + '+';
            clearInterval(timer);
        } else {
            el.textContent = Math.floor(start) + '+';
        }
    }, 16);
}

// Animate hero counters when visible
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const counters = entry.target.querySelectorAll('.fw-bold.text-light.fs-4');
            counters.forEach(counter => {
                const target = parseInt(counter.textContent);
                if (!isNaN(target) && !counter.dataset.animated) {
                    counter.dataset.animated = 'true';
                    animateCounter(counter, target);
                }
            });
        }
    });
}, { threshold: 0.5 });

const heroSection = document.getElementById('home');
if (heroSection) observer.observe(heroSection);
