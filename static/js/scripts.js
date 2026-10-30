// Function to validate the form
function validateForm() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const errorModal = document.getElementById("errorModal");
    const modalMessage = document.getElementById("modalMessage");

    if (username === "" || password === "") {
        // Show the modal with the error message
        modalMessage.textContent = "Username and password are required!";
        errorModal.style.display = "block";
        return false; // Prevent form submission
    }

    return true; // Allow form submission
}

// Handling the OK button in the error modal
const okBtn = document.getElementById("okBtn");
    if (okBtn) {
        okBtn.onclick = function() {
            const errorModal = document.getElementById("errorModal");
            if (errorModal) {
                errorModal.style.display = "none"; // Close the error modal on OK click
            }
        };
    }

// Close the error modal if clicked outside the modal content
window.onclick = function(event) {
    const errorModal = document.getElementById("errorModal");
    if (event.target === errorModal) {
        errorModal.style.display = "none";
    }
};




