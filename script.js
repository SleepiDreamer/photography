

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
var previewImages = document.querySelectorAll("img");
var modalImageUrls = [];

for (var i = 0; i < previewImages.length; i++) {
  var previewSrc = previewImages[i].getAttribute("src");
  var modalSrc = previewSrc.replace("preview/", "modal/");
  modalImageUrls.push(modalSrc);
}

const preloadImage = src => 
new Promise((resolve, reject) => {
  const image = new Image()
  image.onload = resolve
  image.onerror = reject
  image.src = src
})

for (var i = 0; i < modalImageUrls.length; i++) {
  preloadImage(modalImageUrls[i]);
}

window.addEventListener("load", function() {
  var photos = document.querySelectorAll(".photo");
  for (var i = 0; i < photos.length; i++) {
    photos[i].style.opacity = "1";
  }
});





const filterButtons = document.querySelectorAll('.filter-button');
const photos = document.querySelectorAll('.photo');

filterButtons.forEach(button => {
  button.addEventListener('click', () => {
    const filter = button.dataset.filter;
    photos.forEach(photo => {
      const img = photo.querySelector('img')
      if (filter == 'all' || img.classList.contains(filter)) {
        photo.style.display = 'block';
      } else {
        photo.style.display = 'none';
      }
    });
  });
});