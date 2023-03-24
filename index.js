// Get the modal element
var modal = document.getElementById('modal');

// Get the modal image element
var modalImg = document.getElementById("modal-content");

// Get all images with class 'gallery-image'
var images = document.querySelectorAll('.gallery-image');

// Add an event listener to each image
images.forEach(function(image) {
  image.addEventListener('click', function() {
    // Set the source of the modal image to the source of the clicked image
    modalImg.src = this.src;
    // Display the modal
    modal.style.display = "block";
  });
});

// Get the element that closes the modal
var modalClose = document.getElementById('modal-close');

// Add an event listener to close the modal when clicked
modalClose.addEventListener('click', function() { 
  modal.style.display = "none";
});