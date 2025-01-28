// Modal functionality with animation
const portfolioItems = document.querySelectorAll('.portfolio-item');
const modals = document.querySelectorAll('.modal');
const closeButtons = document.querySelectorAll('.modal-close');

portfolioItems.forEach(item => {
  item.addEventListener('click', () => {
    const modalId = item.getAttribute('data-modal');
    const modal = document.getElementById(modalId);

    // Get the card's bounding box for animation
    const rect = item.getBoundingClientRect();

    // Set the modal's initial position to match the card
    modal.style.display = 'flex';
    const modalContent = modal.querySelector('.modal-content');
    modalContent.style.transform = `translate(${rect.left}px, ${rect.top}px) scale(0.5)`;

    // Animate to fullscreen
    setTimeout(() => {
      modal.classList.add('open');
      modalContent.style.transform = 'translate(0, 0) scale(1)';
    }, 10); // Timeout ensures the animation runs
  });
});

closeButtons.forEach(button => {
  button.addEventListener('click', () => {
    const modal = button.closest('.modal');
    const modalContent = modal.querySelector('.modal-content');

    // Animate back to the card
    modalContent.style.transform = 'scale(0.5)';
    modal.classList.remove('open');

    // Hide modal after animation
    setTimeout(() => {
      modal.style.display = 'none';
    }, 300); // Match this to the animation duration
  });
});