// ==========================================================================
// 1. GLOBAL STATE & THEME ENGINE
// ==========================================================================
document.addEventListener("DOMContentLoaded", () => {
    initTheme();
    initMobileMenu();
    initTypingAnimation();
    initScrollTracking();
    logTelemetry("home"); // Log baseline landing event
});

function initTheme() {
    const themeToggle = document.getElementById("themeToggle");
    const currentTheme = localStorage.getItem("theme") || "dark";
    
    document.documentElement.setAttribute("data-theme", currentTheme);
    
    themeToggle.addEventListener("click", () => {
        const nextTheme = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
        document.documentElement.setAttribute("data-theme", nextTheme);
        localStorage.setItem("theme", nextTheme);
    });
}

// ==========================================================================
// 2. MOBILE RESPONSIVE NAVIGATION
// ==========================================================================
function initMobileMenu() {
    const menuToggle = document.getElementById("menuToggle");
    const navMenu = document.getElementById("navMenu");
    
    menuToggle.addEventListener("click", () => {
        if (navMenu.style.display === "flex") {
            navMenu.style.display = "none";
            menuToggle.textContent = "☰";
        } else {
            navMenu.style.display = "flex";
            navMenu.style.flexDirection = "column";
            navMenu.style.position = "absolute";
            navMenu.style.top = "70px";
            navMenu.style.left = "0";
            navMenu.style.width = "100%";
            navMenu.style.backgroundColor = "var(--bg-surface)";
            navMenu.style.padding = "2rem";
            navMenu.style.gap = "1.5rem";
            menuToggle.textContent = "✕";
        }
    });
}

// ==========================================================================
// 3. TYPING EFFECT CORE LOGIC
// ==========================================================================
function initTypingAnimation() {
    const words = ["LLM Applications", "Agentic Workflows", "RAG Systems", "Backend APIs"];
    let wordIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    const targetElement = document.getElementById("typing-text");
    
    function type() {
        const currentWord = words[wordIndex];
        if (isDeleting) {
            targetElement.textContent = currentWord.substring(0, charIndex - 1);
            charIndex--;
        } else {
            targetElement.textContent = currentWord.substring(0, charIndex + 1);
            charIndex++;
        }
        
        let typeSpeed = isDeleting ? 50 : 150;
        
        if (!isDeleting && charIndex === currentWord.length) {
            typeSpeed = 2000; // Pause at completion
            isDeleting = true;
        } else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            wordIndex = (wordIndex + 1) % words.length;
            typeSpeed = 500; // Pause before typing next word
        }
        
        setTimeout(type, typeSpeed);
    }
    
    if (targetElement) type();
}

// ==========================================================================
// 4. TELEMETRY RECORDING & VIEWPORT SCROLL DETECTION
// ==========================================================================
function initScrollTracking() {
    const sections = document.querySelectorAll("section");
    const navLinks = document.querySelectorAll(".nav-link");
    let activeSection = "home";
    
    window.addEventListener("scroll", () => {
        let current = "";
        sections.forEach((section) => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (pageYOffset >= sectionTop - sectionHeight / 3) {
                current = section.getAttribute("id");
            }
        });
        
        if (current && current !== activeSection) {
            activeSection = current;
            navLinks.forEach((link) => {
                link.classList.remove("active");
                if (link.getAttribute("href") === `#${current}`) {
                    link.classList.add("active");
                }
            });
            logTelemetry(current);
        }
    });
}

async function logTelemetry(sectionId) {
    const payload = {
        device: navigator.userAgent.substring(0, 95),
        page_section: sectionId
    };
    
    try {
        const response = await fetch("http://localhost:8000/api/v1/telemetry/log", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        if (response.ok) {
            const data = await response.json();
            const counterElement = document.getElementById("visitorCounter");
            if (counterElement && data.total_visitors) {
                counterElement.textContent = String(data.total_visitors).padStart(6, '0');
            }
        }
    } catch (err) {
        console.warn("Telemetry connection skipped or backend offline.");
    }
}