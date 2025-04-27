navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    document.getElementById('video').srcObject = stream;
  })
  .catch(error => {
    console.error('Camera access error:', error);
  });
