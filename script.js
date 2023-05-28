

// Get all the images on the page
var images = document.querySelectorAll("img");

// Loop through each image and add a click event listener
for (var i = 0; i < images.length; i++) {
  images[i].addEventListener("click", function() {
    // Create a new modal element
    var modal = document.createElement("div");
    modal.classList.add("modal");

    // Create a new image element inside the modal
    var modalImg = document.createElement("img");
    modalImg.src = this.src.replace("/preview/", "/modal/");
    modal.appendChild(modalImg);

    // Add the modal to the page
    document.body.appendChild(modal);

    // Add a click event listener to the modal to close it
    modal.addEventListener("click", function() {
      modal.classList.remove("show");
      setTimeout(function() {
        modal.remove();
      }, 300);
    });

    // Show the modal with an animation
    setTimeout(function() {
      modal.classList.add("show");
    }, 10);
  });
}

// Preload images
var images = document.querySelectorAll(".photo-gallery img");
for (var i = 0; i < images.length; i++) {
  var img = new Image();
  img.src = images[i].src;
}

window.addEventListener("load", function() {
  var photos = document.querySelectorAll(".photo");
  for (var i = 0; i < photos.length; i++) {
    photos[i].style.opacity = "1";
  }
});

fetch("/modal/")
  .then(response => response.text())
  .then(data => {
    var parser = new DOMParser();
    var html = parser.parseFromString(data, "text/html");
    var images = html.querySelectorAll("a[href$='.jpg'], a[href$='.jpeg'], a[href$='.png'], a[href$='.gif']");

    // Loop through each image and create an img element with the src attribute set to the image URL
    for (var i = 0; i < images.length; i++) {
      var img = document.createElement("img");
      img.src = images[i].href;
      img.style.display = "none";
      document.body.appendChild(img);
    }
  });