const burgerButton = document.querySelector('.burger-btn');
const mobileMenu = document.querySelector('.mobile-menu');
const overlay = document.querySelector('.mobile-menu-overlay');
const body = document.body;

function toggleMenu() {
  overlay.classList.toggle('active');
  mobileMenu.classList.toggle('active');
  body.classList.toggle('no-scroll');
}

const headerHeight = 70; // Adjust this to match your header height
let isOverlayAtTop = false;

window.addEventListener('scroll', () => {
  const scrollPosition = window.scrollY;

  if (scrollPosition > headerHeight && !isOverlayAtTop) {
    // If scrolled past the header, move the overlay to cover the entire screen
    overlay.style.top = '0';
    overlay.style.height = '100%';
    isOverlayAtTop = true;
  } else if (scrollPosition <= headerHeight && isOverlayAtTop) {
    // If back to the top, position the overlay below the header
    overlay.style.top = `${headerHeight}px`;
    overlay.style.height = `calc(100% - ${headerHeight}px)`;
    isOverlayAtTop = false;
  }
});
