// Function to submit a fortune when the button is clicked
document.getElementById('submit-fortune-btn').addEventListener('click', function() {
    // Get the value of the input field
    const fortune = document.getElementById('fortune-input').value;

    // Make an HTTP POST request to submit the fortune
    fetch('https://ywtzp7u3v9.execute-api.us-east-1.amazonaws.com/Test/Fortune-Lambda', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ Fortunes: fortune })
    })
    .then(response => response.json())
    .then(data => {
        // Log success message
        console.log('Fortune submitted successfully:', data);
    })
    .catch(error => {
        // Handle any errors
        console.error('Error submitting fortune:', error);
    });
});

// Function to retrieve a random fortune when the button is clicked
document.getElementById('get-fortune-btn').addEventListener('click', function() {
    // Make an HTTP GET request to retrieve a random fortune
    fetch('https://ywtzp7u3v9.execute-api.us-east-1.amazonaws.com/Test/Fortune-Lambda', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        // Log success message
        console.log('Fortune retrieved successfully:', data);
        // Display the retrieved fortune
        document.getElementById('fortune-container').innerHTML = `<p>${data.message}: ${data.Fortunes}</p>`;
    })
    .catch(error => {
        // Handle any errors
        console.error('Error retrieving fortune:', error);
    });
});


