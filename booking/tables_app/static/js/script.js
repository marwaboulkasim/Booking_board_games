document.addEventListener("DOMContentLoaded", function() {
    console.log("JS calendar.js chargé");

    const bookingForm = document.getElementById("bookingForm");
    const bookingModal = new bootstrap.Modal(document.getElementById('bookingModal'));

    // Déclencheur sur les boutons "Réserver"
    document.querySelectorAll(".reserve-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            const tableId = btn.dataset.tableId;
            const date = btn.dataset.date;

            console.log("Réserver clic :", tableId, date);

            // Remplir les inputs cachés
            document.getElementById("table_id").value = tableId;
            document.getElementById("date_input").value = date;

            // Mettre à jour l'action du formulaire
            bookingForm.action = `/users/create-booking/${tableId}/`;


            // Ouvrir le modal
            bookingModal.show();
        });
    });
});
