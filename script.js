function layoutImages(callback){
  gallery = $('#gallery'); // cache a reference to our container
  imagelist = $('#gallery img'); // cache a reference to our image list
  var horizontalGap = 0.01 * screen.width;
  var verticalGap = horizontalGap;
  var containerWidth = gallery.width();
  var columncount = 3; // or any other number of columns you want to display
  if (screen.width <= 767) {
    columncount = 1; // set number of columns to 1 for mobile devices
    verticalGap = 15;
  }
  var fixedwidth = containerWidth / columncount + horizontalGap;
  columns = [];

  for (var i =0;i<columncount;i++){ // initialize columns (0 height for each)
      columns.push(0);
  }

  imagelist.each(function(i,image){
      if ($(image).is(':hidden')) { // check if the image is hidden
        $(image).addClass('bottom'); // add a class to the hidden image
        $(image).css({top: gallery.height()}); // set the top property of the hidden image to the height of the container element
      } else {
        var min = Math.min.apply(null, columns), // find height of shortest column
            index = columns.indexOf(min), // find column number with the min height
            x = index*fixedwidth; // calculate horizontal position of current image based on column it belongs

        columns[index] += image.height + verticalGap; //calculate new height of column
        $(image).css({left:x, top:min}).delay(0).animate({},100, function() {
          // call the callback function after the animation is complete
          if (i === imagelist.length - 1) {
            callback();
          }
        }); // assign new position to image and show it
      }
  });
}


function debounce(func, wait) {
  var timeout;
  return function() {
    var context = this, args = arguments;
    clearTimeout(timeout);
    timeout = setTimeout(function() {
      timeout = null;
      func.apply(context, args);
    }, wait);
  };
}




$(window).on('load', function(){
  layoutImages(function() {
    // hide the loading screen when the images have finished loading and the layout is complete
    $('#loading-screen').hide();
  });
  $(window).resize(debounce(layoutImages, 100));
  $(window).on('orientationchange', debounce(layoutImages, 100));
});

window.addEventListener("deviceorientation", function(event) {
  layoutImages();
}, true);

// Get all the images on the page
var images = document.querySelectorAll("img");

// Loop through each image and add a click event listener
for (var i = 0; i < images.length; i++) {
  images[i].addEventListener("click", function() {
    // Find the index of the clicked image
    var index = Array.prototype.indexOf.call(images, this);

    // Create a new modal element
    var modal = document.createElement("div");
    modal.classList.add("modal");

    // Create a new image element inside the modal
    var modalImg = document.createElement("img");
    modalImg.src = this.src.replace("/preview/", "/modal/");
    modal.appendChild(modalImg);

    if (screen.width >= 767) {
      // Create left arrow button
      var leftButton = document.createElement("div");
      leftButton.classList.add("modal-arrow-button", "modal-arrow-left");
      leftButton.innerHTML = "&#10094;";
      modal.appendChild(leftButton);

      // Create right arrow button
      var rightButton = document.createElement("div");
      rightButton.classList.add("modal-arrow-button", "modal-arrow-right");
      rightButton.innerHTML = "&#10095;";
      modal.appendChild(rightButton);
    }

    
    // Create close button
    var closeButton = document.createElement("div");
    closeButton.classList.add("modal-close-button");
    closeButton.innerHTML = "&#10005;";
    modal.appendChild(closeButton);

    // Add the modal to the page
    document.body.appendChild(modal);

    // Add a click event listener to the close button to close the modal
    closeButton.addEventListener("click", function() {
      closeModal();
    });

    if (screen.width >= 767) {
      // Add a click event listener to the left arrow button to show the previous image
      leftButton.addEventListener("click", function() {
        var prevImage = images[index - 1];
        if (prevImage) {
          modalImg.src = prevImage.src.replace("/preview/", "/modal/");
          index--;
        }
      });

      // Add a click event listener to the right arrow button to show the next image
      rightButton.addEventListener("click", function() {
        var nextImage = images[index + 1];
        if (nextImage) {
          modalImg.src = nextImage.src.replace("/preview/", "/modal/");
          index++;
        }
      });
    }

    // Add a keydown event listener to the document to close the modal when the Escape key is pressed
    document.addEventListener("keydown", function(event) {
      if (event.key === "Escape") {
        closeModal();
      } else if (event.key === "ArrowLeft") {
        var prevImage = images[index - 1];
        if (prevImage) {
          modalImg.src = prevImage.src.replace("/preview/", "/modal/");
          index--;
        }
      } else if (event.key === "ArrowRight") {
        var nextImage = images[index + 1];
        if (nextImage) {
          modalImg.src = nextImage.src.replace("/preview/", "/modal/");
          index++;
        }
      }
    });

    // Show the modal with an animation
    setTimeout(function() {
      modal.classList.add("show");
    }, 10);

    // Function to close the modal
    function closeModal() {
      modal.classList.remove("show");
      setTimeout(function() {
        modal.remove();
      }, 300);
    }
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

const filterButtons = document.querySelectorAll('.filter-button');
const photos = document.querySelectorAll('#gallery img');

filterButtons.forEach(button => {
  button.addEventListener('click', () => {
    const filter = button.dataset.filter;
    photos.forEach(photo => {
      if (filter == 'all' || photo.classList.contains(filter)) {
        photo.style.display = 'inline-block';
      } else {
        photo.style.display = 'none';
      }
    });
    layoutImages();
  });
});



if (false) {
  if (screen.width <= 767) {
    $(document).ready(function() {
      var $window = $(window);
      var $images = $('#gallery img');
      var windowHeight = $window.height();
      var windowWidth = $window.width();

      function updateCarousel() {
        var scrollTop = $window.scrollTop();
        var center = scrollTop + windowHeight / 2;

        $images.each(function() {
          var $image = $(this);
          var imageTop = $image.offset().top;
          var imageHeight = $image.height();
          var distanceTop = Math.abs(center - imageTop);
          if (distanceTop < windowHeight) {
            var distanceCentre = Math.abs(center - (imageTop + imageHeight / 2));
            var distanceBottom = Math.abs(center - (imageTop + imageHeight));
            if (center - (imageTop + imageHeight) < 0) {
              var distance = Math.min(distanceTop, distanceCentre, distanceBottom);
              var maxDistance = windowHeight * 1.5;
              var scale = ((1.5 - (distance / maxDistance)) / 1.5) + 0.1;
              var opacity = ((1.5 - (distance / maxDistance)) / 1.5) + 0.1;

              if (scale < 0.8) {
                scale = 0.8;
              }
              if (scale > 1.0) {
                scale = 1.0;
              }
              if (opacity < 0.8) {
                opacity = 0.8;
              }

              $image.css('transform', 'scale(' + scale + ')');
              $image.css('opacity', opacity);
            }
          }
        });
      }

      $window.on('scroll', updateCarousel);

      $('.filter-button').on('click', function() {
        var filter = $(this).data('filter');
        $('#gallery img').hide();
        if (filter === 'all') {
          $('#gallery img').show();
        } else {
          $('#gallery img.' + filter).show();
        }
        updateCarousel();
      });
    });
  }
}