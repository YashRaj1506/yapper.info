document.getElementById('submit-btn').addEventListener('click', function() {
    const username = document.querySelector('input').value.trim();
    if (username) {
      alert(`Calculating Yapper Score for @${username}... This would connect to your backend in a real implementation.`);
      // In a real implementation, this would make an API call to your backend
    } else {
      alert('Please enter a Twitter username');
    }
  });