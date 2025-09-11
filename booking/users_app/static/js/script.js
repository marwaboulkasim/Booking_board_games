document.addEventListener("DOMContentLoaded", function() {
    console.log("JS calendar.js chargé");

    const modal = document.getElementById("bookingModal");
    const form = document.getElementById("bookingForm");

    if (!modal || !form) {
        console.error("Modal ou formulaire introuvable !");
        return;
    }

    const close = modal.querySelector(".close");
    if (!close) {
        console.error("Bouton de fermeture introuvable !");
        return;
    }

    // Ouvrir le modal
    document.querySelectorAll(".reserve-btn").forEach(btn => {
        console.log("Bouton détecté :", btn); // DEBUG

        btn.addEventListener("click", () => {
            const tableId = btn.dataset.tableId;
            const date = btn.dataset.date;

            console.log("Réserver clic :", tableId, date); // DEBUG

            // Remplir les inputs cachés
            const tableInput = document.getElementById("table_id");
            const dateInput = document.getElementById("date_input");

            if (tableInput) tableInput.value = tableId;
            if (dateInput) dateInput.value = date;

            // Action dynamique du formulaire
            form.action = `/users/create-booking/${tableId}/`;

            // Afficher le modal
            modal.style.display = "block";
        });
    });

    // Fermer le modal avec la croix
    close.addEventListener("click", () => {
        modal.style.display = "none";
        console.log("Modal fermé (croix)");
    });

    // Fermer le modal si clic en dehors
    window.addEventListener("click", (e) => {
        if (e.target == modal) {
            modal.style.display = "none";
            console.log("Modal fermé (clic en dehors)");
        }
    });
});
