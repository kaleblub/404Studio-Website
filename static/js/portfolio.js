document.addEventListener('DOMContentLoaded', () => {
    const portfolioItems = document.querySelectorAll('.portfolio-item');

    portfolioItems.forEach((item, index) => {
        item.addEventListener('click', () => {
            // Expand the clicked card
            item.classList.add('active');

            const button = item.querySelector('.close-btn');
            if (button) {
                button.classList.add('button', 'button--quidel', 'button--inverted');
            }

            // Disable scrolling on the body
            document.body.style.overflow = 'hidden';
        });

        const closeButton = item.querySelector('.close-btn');
        if (closeButton) {
        closeButton.addEventListener('click', (e) => {
            e.stopPropagation();
            // console.log('Close button clicked');
            item.classList.remove('active');
            document.body.style.overflow = 'auto';
        });
        } else {
        console.log(`No close button found in item ${index}`);
        }
    });
});