function layoutImages(callback){
  gallery = $('#gallery'), // cache a reference to our container
  imagelist = $('#gallery img:visible'); // cache a reference to our image list
  var horizontalGap = 0.01 * screen.width;
  var verticalGap = horizontalGap;
  var containerWidth = gallery.width();
  var columncount = 3; // or any other number of columns you want to display
  if (screen.width <= 767) {
    columncount = 1; // set number of columns to 1 for mobile devices
    verticalGap = 15
  }
  var fixedwidth = containerWidth / columncount + horizontalGap;
  columns = [];

  for (var i =0;i<columncount;i++){ // initialize columns (0 height for each)
      columns.push(0);
  }

  imagelist.each(function(i,image){
        var min = Math.min.apply(null, columns), // find height of shortest column
            index = columns.indexOf(min), // find column number with the min height
            x = index*fixedwidth; // calculate horizontal position of current image based on column it belongs

      columns[index] += image.height + verticalGap; //calculate new height of column
      $(image).css({left:x, top:min}).delay(i*1).animate({opacity:1},100); // assign new position to image and show it
      $(image).css({left:x, top:min}).delay(i*1).animate({opacity:1},100, function() {
        // call the callback function after the animation is complete
        if (i === imagelist.length - 1) {
          callback();
        }
      });
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
    console.log("yes");
  });
  $(window).resize(debounce(layoutImages, 100));
});





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