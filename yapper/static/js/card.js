document.addEventListener('DOMContentLoaded', function() {
  const username = document.getElementById('username').textContent;
  const score = document.getElementById('yapper-score').textContent;
  const tweetText = `I just got a Yapper Score of ${score}! How much of a yapper are you on Twitter? #YapperScore`;
  const websiteUrl = "yapperkai.pythonanywhere.com";
  
  // Handle profile image for better rendering
  const profileImage = document.getElementById('profile-image');
  if (profileImage) {
    profileImage.crossOrigin = "anonymous";
  }
  
  // Load html2canvas dynamically
  function loadHtml2Canvas() {
    return new Promise((resolve, reject) => {
      if (window.html2canvas) {
        resolve(window.html2canvas);
        return;
      }
      
      const script = document.createElement('script');
      script.src = 'https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js';
      script.onload = () => resolve(window.html2canvas);
      script.onerror = () => reject(new Error('Failed to load html2canvas'));
      document.head.appendChild(script);
    });
  }
  
  // Function to show loading indicator
  function showLoading() {
    const container = document.querySelector('.card-wrapper');
    const loadingEl = document.createElement('div');
    loadingEl.id = 'card-loading-indicator';
    loadingEl.innerHTML = 'Creating image...';
    loadingEl.style.position = 'fixed';
    loadingEl.style.top = '50%';
    loadingEl.style.left = '50%';
    loadingEl.style.transform = 'translate(-50%, -50%)';
    loadingEl.style.backgroundColor = 'rgba(0,0,0,0.7)';
    loadingEl.style.color = 'white';
    loadingEl.style.padding = '10px 20px';
    loadingEl.style.borderRadius = '20px';
    loadingEl.style.zIndex = '999';
    document.body.appendChild(loadingEl);
    return loadingEl;
  }
  
  // Function to remove loading indicator
  function hideLoading(loadingEl) {
    if (loadingEl && document.body.contains(loadingEl)) {
      document.body.removeChild(loadingEl);
    }
  }
  
  // Function to create a screenshot with optimal settings
  async function captureCard() {
    const loadingEl = showLoading();
    
    try {
      // Load html2canvas if not already loaded
      const html2canvas = await loadHtml2Canvas();
      
      // Capture the card
      const card = document.getElementById('yapper-card');
      const canvas = await html2canvas(card, {
        backgroundColor: null,
        allowTaint: true,
        useCORS: true,
        scale: 2,
        logging: false
      });
      
      // Hide loading indicator
      hideLoading(loadingEl);
      
      return canvas;
    } catch (error) {
      // Hide loading indicator on error
      hideLoading(loadingEl);
      console.error('Error capturing card:', error);
      alert('Sorry, there was an error creating the image. Please try taking a screenshot manually.');
      throw error;
    }
  }
  
  // Download button functionality
  document.getElementById('download-btn').addEventListener('click', async function() {
    try {
      const canvas = await captureCard();
      
      // Create a download link
      const link = document.createElement('a');
      link.download = `yapper-score-${username}.png`;
      link.href = canvas.toDataURL('image/png');
      link.click();
    } catch (error) {
      console.error('Error downloading card:', error);
    }
  });
  
  // Twitter share button
  document.getElementById('tweet-btn').addEventListener('click', async function() {
    try {
      const canvas = await captureCard();
      
      // Create a download link and auto-download the image
      const link = document.createElement('a');
      link.download = `yapper-score-${username}.png`;
      link.href = canvas.toDataURL('image/png');
      link.click();
      
      // After a small delay, open Twitter with pre-filled text
      setTimeout(function() {
        // Construct the Twitter share URL with text and website URL as separate parameters
        const twitterUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(tweetText)}&url=https://${encodeURIComponent(websiteUrl)}`;
        window.open(twitterUrl, '_blank');
      }, 500);
    } catch (error) {
      console.error('Error sharing on Twitter:', error);
    }
  });
});