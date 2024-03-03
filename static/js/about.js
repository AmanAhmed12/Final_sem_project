AOS.init();
// You can also pass an optional settings object
// below listed default settings
AOS.init({
 

  // Settings that can be overridden on per-element basis, by `data-aos-*` attributes:
  offset: 120, // offset (in px) from the original trigger point
  delay: 0, // values from 0 to 3000, with step 50ms
  duration: 700, // values from 0 to 3000, with step 50ms
  easing: 'ease', // default easing for AOS animations
  once: false, // whether animation should happen only once - while scrolling down
  mirror: false, // whether elements should animate out while scrolling past them
  anchorPlacement: 'top-bottom', // defines which position of the element regarding to window should trigger the animation

});



// Function to handle download link click
function downloadCv(event) {
  // Prevent the default behavior of the link click, which is to navigate to the URL
  event.preventDefault();

  // Get the href attribute of the clicked link (which is the PDF file URL)
  var pdfUrl = event.target.href;
  
  // Create an anchor element
  var link = document.createElement('a');
  
  // Set the href attribute to the PDF file's URL
  link.href = pdfUrl;
  
  // Set the download attribute to specify the file's name
  link.download = 'Resume.pdf';
  
  // Append the anchor element to the document body
  document.body.appendChild(link);
  
  // Trigger a click event on the anchor element
  link.click();
  
  // Remove the anchor element from the document body
  document.body.removeChild(link);
}

// Get the download link element
var downloadLink = document.getElementById('downloadLink');

// Attach an event listener to the download link
downloadLink.addEventListener('click', downloadCv);


function sendEmail() {
  var name = document.querySelector('#contactForm [name="name"]').value;
  var email = document.querySelector('#contactForm [name="email"]').value;
  var subject = document.querySelector('#contactForm [name="subject"]').value;
  var message = document.querySelector('#contactForm [name="message"]').value;

  // Construct mailto link
  var mailtoLink = "mailto:ananahd1000@gmail.com";
  mailtoLink += "?subject=" + encodeURIComponent(subject);
  mailtoLink += "&body=" + encodeURIComponent(message);

  console.log("Mailto link:", mailtoLink); // Check the generated mailto link in the console

  // Open default email client
  window.location.href = mailtoLink;
}

let status = false;

function changeThemeLight() {
  var content = document.getElementById("content-wrapper");
  var home = document.getElementById("home");
  var heads = document.getElementsByClassName("head");
  var white= document.getElementsByClassName("white");
  var h1=document.getElementsByTagName("h1");
  var h6=document.getElementsByTagName("h6");
  var h3=document.getElementsByTagName("h3");
  var foot= document.getElementById("foot");

  foot.style.color="black";

  for (var i = 0; i < h3.length; i++) {
    h3[i].style.color = "#033f47";
  }

  for (var i = 0; i < h6.length; i++) {
    h6[i].style.color = "#033f47";
  }

  for (var i = 0; i < h1.length; i++) {
    h1[i].style.color = "black";
  }

  for (var i = 0; i < white.length; i++) {
    white[i].style.color = "black";
  }

  for (var i = 0; i < heads.length; i++) {
    heads[i].style.color = "black";
  }

  home.style.background="white";
  home.style.backgroundColor="white";
 
  
  
  content.style.backgroundColor = "#ECF3F9";
  status = true; // Update status to true
}

function changeThemeDark() {
  var content = document.getElementById("content-wrapper");
  content.style.backgroundColor = "#022a30";
  var home = document.getElementById("home");
  var heads = document.getElementsByClassName("head");
  var white= document.getElementsByClassName("white");
  var h1=document.getElementsByTagName("h1");
  var h6=document.getElementsByTagName("h6");
  var h3=document.getElementsByTagName("h3");
  var foot= document.getElementById("foot");

  foot.style.color="#ECF3F9";

  for (var i = 0; i < h3.length; i++) {
    h3[i].style.color = "white";
  }

  

  for (var i = 0; i < h6.length; i++) {
    h6[i].style.color = "#e0f780";
  }


  for (var i = 0; i < h1.length; i++) {
    h1[i].style.color = "white";
  }

  for (var i = 0; i < white.length; i++) {
    white[i].style.color = "white";
  }

  for (var i = 0; i < heads.length; i++) {
    heads[i].style.color = "#e0f780";
  }

  home.style.background="#022a30";
  home.style.backgroundColor="#022a30";
 
 
  status = false; // Update status to false
}

// Get the theme button element
var theme = document.getElementById('themeBtn');

// Attach an event listener to the theme button
theme.addEventListener('click', function() {
  if (status) {
    changeThemeDark(); // If status is true, change to dark theme
  } else {
    changeThemeLight(); // If status is false, change to light theme
  }
});




