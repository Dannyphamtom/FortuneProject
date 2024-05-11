document.getElementById('get-fortune-btn').addEventListener('click', function() {
    fetch('https://ywtzp7u3v9.execute-api.us-east-1.amazonaws.com/Test/Fortune-Lambda')
        .then(response => response.json())
        .then(data => {
            const fortune = data.Fortunes && data.Fortunes.S; // Check if Fortunes exists before accessing S
            if (fortune) {
                document.getElementById('fortune-container').innerHTML = `<p>${fortune}</p>`;
            } else {
                document.getElementById('fortune-container').innerHTML = `<p>No fortune available</p>`;
            }
        })
        .catch(error => {
            console.error('Error fetching fortune:', error);
            document.getElementById('fortune-container').innerHTML = `<p>Error fetching fortune</p>`;
        });
});


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
