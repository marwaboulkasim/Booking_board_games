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


function openBookingModal(tableId, date) {
    document.getElementById('table_id').value = tableId;
    document.getElementById('date_input').value = date;
    document.getElementById('bookingForm').action = `/users/create-booking/${tableId}/`; // mise à jour dynamique de l'action
    document.getElementById('bookingModal').style.display = 'block';
}

function closeBookingModal() {
    document.getElementById('bookingModal').style.display = 'none';
}

// Fermer le modal si clic en dehors
window.onclick = function(event) {
    let modal = document.getElementById('bookingModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}
