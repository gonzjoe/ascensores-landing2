/**
 * Ascensores Wolf Group - Industrial Luxury Landing Page
 * Enhanced interactions and animations
 */

(function() {
    'use strict';

    // Custom Cursor removed for compatibility (v2.4)

    // ============================================
    // Mobile Menu Toggle
    // ============================================
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const mobileMenu = document.querySelector('.mobile-menu');
    const mobileMenuLinks = document.querySelectorAll('.mobile-menu__link');

    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            const isOpen = this.getAttribute('aria-expanded') === 'true';
            this.setAttribute('aria-expanded', !isOpen);
            mobileMenu.classList.toggle('is-open');
            mobileMenu.setAttribute('aria-hidden', isOpen);
            document.body.style.overflow = isOpen ? '' : 'hidden';
        });

        mobileMenuLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                const target = this.getAttribute('href');
                
                // Forzar navegación explícita para evitar que iOS Safari aborte
                // el evento de enlace al removerse la visibilidad de la clase.
                if (target && !target.startsWith('#')) {
                    e.preventDefault();
                    setTimeout(() => {
                        window.location.href = target;
                    }, 50);
                }
                
                mobileMenuBtn.setAttribute('aria-expanded', 'false');
                mobileMenu.classList.remove('is-open');
                mobileMenu.setAttribute('aria-hidden', 'true');
                document.body.style.overflow = '';
            });
        });

        document.addEventListener('keydown', e => {
            if (e.key === 'Escape' && mobileMenu.classList.contains('is-open')) {
                mobileMenuBtn.setAttribute('aria-expanded', 'false');
                mobileMenu.classList.remove('is-open');
                mobileMenu.setAttribute('aria-hidden', 'true');
                document.body.style.overflow = '';
                mobileMenuBtn.focus();
            }
        });
    }

    // ============================================
    // Header Scroll Effect
    // ============================================
    const header = document.querySelector('.header');
    if (header) {
        let lastScroll = 0;
        window.addEventListener('scroll', () => {
            const currentScroll = window.pageYOffset;
            if (currentScroll > 50) {
                header.classList.add('header--scrolled');
            } else {
                header.classList.remove('header--scrolled');
            }
            lastScroll = currentScroll;
        }, { passive: true });
    }

    // ============================================
    // Smooth Scroll
    // ============================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                const headerHeight = header ? header.offsetHeight : 0;
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - headerHeight;
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // ============================================
    // Stats Counter Animation
    // ============================================
    const statNumbers = document.querySelectorAll('.stat__number[data-target]');
    let statsAnimated = false;

    const animateStats = () => {
        statNumbers.forEach(stat => {
            const target = parseInt(stat.dataset.target);
            const duration = 2000;
            const startTime = performance.now();

            const updateNumber = (currentTime) => {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                const easeOut = 1 - Math.pow(1 - progress, 3);
                const current = Math.floor(easeOut * target);

                stat.textContent = current;

                if (progress < 1) {
                    requestAnimationFrame(updateNumber);
                }
            };

            requestAnimationFrame(updateNumber);
        });
    };

    // ============================================
    // Intersection Observer for Animations
    // ============================================
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target);

                // Trigger stats animation when stats section is visible
                if (entry.target.classList.contains('stats') && !statsAnimated) {
                    statsAnimated = true;
                    setTimeout(animateStats, 300);
                }
            }
        });
    }, observerOptions);

    // Observe elements
    document.querySelectorAll('.servicio-card, .feature, .testimonial, .stats').forEach(el => {
        el.classList.add('fade-in');
        observer.observe(el);
    });

    // ============================================
    // Form Validation
    // ============================================
    const contactForm = document.getElementById('contact-form');

    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const requiredFields = this.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#ef4444';
                } else {
                    field.style.borderColor = '';
                }
            });

            if (!isValid) {
                // Shake animation
                this.style.animation = 'shake 0.5s ease';
                setTimeout(() => {
                    this.style.animation = '';
                }, 500);
            } else {
                // Ejecutar reCAPTCHA invisible v3
                if (typeof grecaptcha !== 'undefined') {
                    grecaptcha.ready(function() {
                        grecaptcha.execute('6LcSjpMsAAAAAC7dF4KV2XgQzF5GIO-jz1tFzl4i', {action: 'submit'}).then(function(token) {
                            // Asignar token al campo oculto por si acaso
                            document.getElementById('recaptchaToken').value = token;
                            
                            const formData = {
                                name: contactForm.querySelector('#name').value,
                                email: contactForm.querySelector('#email').value,
                                phone: contactForm.querySelector('#phone').value,
                                service: contactForm.querySelector('#service').value,
                                message: contactForm.querySelector('#message').value,
                                recaptchaToken: token
                            };

                            const submitBtn = contactForm.querySelector('button[type="submit"]');
                            const originalText = submitBtn.innerHTML;
                            submitBtn.innerHTML = '<span>Enviando...</span>';
                            submitBtn.disabled = true;

                            fetch('enviar_correo.php', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json'
                                },
                                body: JSON.stringify(formData)
                            })
                            .then(response => response.json())
                            .then(data => {
                                if (data.status === 'success') {
                                    submitBtn.innerHTML = '<span>Enviado</span>';
                                    submitBtn.style.background = '#10b981';
                                    submitBtn.style.color = '#fff';
                                    contactForm.reset();
                                } else {
                                    alert('Hubo un error al enviar el mensaje: ' + data.message);
                                    submitBtn.innerHTML = originalText;
                                    submitBtn.disabled = false;
                                }
                            })
                            .catch(error => {
                                alert('Ocurrió un error en el servidor. Inténtalo de nuevo.');
                                submitBtn.innerHTML = originalText;
                                submitBtn.disabled = false;
                            })
                            .finally(() => {
                                setTimeout(() => {
                                    if(submitBtn.innerHTML.includes('Enviado')) {
                                        submitBtn.innerHTML = originalText;
                                        submitBtn.style.background = '';
                                        submitBtn.style.color = '';
                                    }
                                    submitBtn.disabled = false;
                                }, 4000);
                            });
                        });
                    });
                } else {
                    console.error("Error: reCAPTCHA no está cargado.");
                }
            }
        });

        contactForm.querySelectorAll('input, textarea, select').forEach(field => {
            field.addEventListener('input', function() {
                this.style.borderColor = '';
            });
        });
    }

    // ============================================
    // Add CSS for shake animation and fade-in
    // ============================================
    const style = document.createElement('style');
    style.textContent = `
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            20% { transform: translateX(-8px); }
            40% { transform: translateX(8px); }
            60% { transform: translateX(-8px); }
            80% { transform: translateX(8px); }
        }

        .fade-in {
            opacity: 0;
            transform: translateY(30px);
            transition: opacity 0.6s ease, transform 0.6s ease;
        }

        .is-visible {
            opacity: 1;
            transform: translateY(0);
        }

        /* Stagger delays for cards */
        .servicio-card:nth-child(1) { transition-delay: 0.1s; }
        .servicio-card:nth-child(2) { transition-delay: 0.2s; }
        .servicio-card:nth-child(3) { transition-delay: 0.3s; }
        .servicio-card:nth-child(4) { transition-delay: 0.4s; }

        .feature:nth-child(1) { transition-delay: 0.1s; }
        .feature:nth-child(2) { transition-delay: 0.15s; }
        .feature:nth-child(3) { transition-delay: 0.2s; }
        .feature:nth-child(4) { transition-delay: 0.25s; }
        .feature:nth-child(5) { transition-delay: 0.3s; }
        .feature:nth-child(6) { transition-delay: 0.35s; }

        .testimonial:nth-child(1) { transition-delay: 0.1s; }
        .testimonial:nth-child(2) { transition-delay: 0.2s; }
        .testimonial:nth-child(3) { transition-delay: 0.3s; }
    `;
    document.head.appendChild(style);

})();