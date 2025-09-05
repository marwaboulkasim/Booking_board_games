// Exemple simple d'interaction JS
document.addEventListener("DOMContentLoaded", function() {
    console.log("JS chargé !");
    
    const buttons = document.querySelectorAll("button");
    buttons.forEach(btn => {
        btn.addEventListener("click", () => {
            btn.style.opacity = 0.8; // petite interaction visuelle
            setTimeout(() => btn.style.opacity = 1, 200);
        });
    });
});
console.log("JS chargé !");
