//show welcome message
function welMsg(){
    const welcomeMessage = document.getElementById("welcomeMessage");
    welcomeMessage.style.display="block";
    setTimeout(()=>{
        welcomeMessage.style.display="none";
    },3000);
}
var log_out = document.getElementById("log_out");

// Get the modal element for profile image click
var popupModal = document.getElementById("popupModal");

// Get the buttons for the profile modal
var yesButton = document.getElementById("yesButton");
var cancelButton = document.getElementById("cancelBtn");

// Show the profile modal on profile image click
log_out.onclick = function() {
    popupModal.style.display = "flex"; // Show the modal
};

// Handle Yes button click inside profile modal (Log out action)
yesButton.onclick = function() {
    alert("Logged out!");
    popupModal.style.display = "none"; // Close the modal after logout
};

// Handle Cancel button click inside profile modal (Close modal)
if (cancelButton) {
        cancelButton.onclick = function() {
            popupModal.style.display = "none"; // Close the modal only on Cancel click
        };
    }

// Close the profile modal if clicked outside the modal content
window.onclick = function(event) {
    const modal = document.getElementById("popupModal");
    if (event.target === modal) {
        modal.style.display = "none";
    }
};