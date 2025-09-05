// script.js
document.addEventListener('DOMContentLoaded', () => {
    const button = document.querySelector('button');
    if (button) {
        button.addEventListener('click', () => {
            alert('Bouton cliqué ! 🎉');
        });
    }
});