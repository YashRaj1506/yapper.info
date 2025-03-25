document.getElementById('yapper-form')?.addEventListener('submit', function() {
    // Show loading message
    document.getElementById('loading-message').style.display = 'block';
    
    // Disable submit button to prevent multiple submissions
    document.getElementById('submit-btn').disabled = true;
    document.getElementById('submit-btn').innerHTML = 'Calculating...';
  });