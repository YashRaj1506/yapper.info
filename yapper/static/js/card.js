document.addEventListener('DOMContentLoaded', function() {
    // Share button functionality
    function copyToClipboard(text) {
      const textarea = document.createElement('textarea');
      textarea.value = text;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand('copy');
      document.body.removeChild(textarea);
      alert('Share text copied to clipboard!');
    }
  });