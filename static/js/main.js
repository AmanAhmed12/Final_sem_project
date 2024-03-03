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


function sendEmail() {
  var nameInput = document.querySelector('#contactForm [name="name"]');
  var emailInput = document.querySelector('#contactForm [name="email"]');
  var subjectInput = document.querySelector('#contactForm [name="subject"]');
  var messageInput = document.querySelector('#contactForm [name="message"]');

  var name = nameInput.value;
  var email = emailInput.value;
  var subject = subjectInput.value;
  var message = messageInput.value;

  // Construct mailto link
  var mailtoLink = "mailto:ananahd1000@gmail.com";
  mailtoLink += "?subject=" + encodeURIComponent(subject);
  mailtoLink += "&body=" + encodeURIComponent(message);

  console.log("Mailto link:", mailtoLink); // Check the generated mailto link in the console

  // Open default email client
  window.location.href = mailtoLink;

  // Clear input fields
  nameInput.value = "";
  emailInput.value = "";
  subjectInput.value = "";
  messageInput.value = "";
}



