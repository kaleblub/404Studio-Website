const burgerButton = document.querySelector('.burger-btn');
const mobileMenu = document.querySelector('.mobile-menu');
const mainNavigation = document.querySelector('.navigation');

// Toggle mobile menu and navigation
burgerButton.addEventListener('click', () => {
  // Toggle the 'active' class on the mobile menu to show/hide it
  mobileMenu.classList.toggle('active');

  // Check if the mobile menu is active and update navigation accordingly
  if (mobileMenu.classList.contains('active')) {
    // When the mobile menu is open, hide the regular navigation
    mainNavigation.style.display = 'none';
  }
});
