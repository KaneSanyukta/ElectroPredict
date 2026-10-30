window.onload = function() {
    // Show the loading spinner and the message
    document.getElementById('loading').style.display = 'block';
    document.getElementById('message').style.display = 'block';

    // Simulate a delay (e.g., 3 seconds) before showing the price prediction message
    setTimeout(function() {
        // Simulating a price prediction result
        document.getElementById('message').textContent = "Price prediction:" + predictionResult; 
        document.getElementById('loading').style.display = 'none';
    }, 5000); // Delay of 3 seconds (3000 milliseconds)
}