// add hovered class to selected list item
let list = document.querySelectorAll(".navigation li");

function activeLink() {
  list.forEach((item) => {
    item.classList.remove("hovered");
  });
  this.classList.add("hovered");
}

list.forEach((item) => item.addEventListener("mouseover", activeLink));

// Menu Toggle
let toggle = document.querySelector(".toggle");
let navigation = document.querySelector(".navigation");
let main = document.querySelector(".main");

toggle.onclick = function () {
  navigation.classList.toggle("active");
  main.classList.toggle("active");
};

function loadCreateAccount() {
  // Load dashboard.html into the content div
  document.getElementById("content").innerHTML = '<iframe src="about.html" frameborder="0" style="width: 100vw; height: 100vh;"></iframe>';
}

function loadDefaultAdminDashboard() {
  // Load dashboard.html into the content div
  document.getElementById("content").innerHTML = '<iframe src="defaultAdminDashContent.html" frameborder="0" style="width: 100vw; height: 100vh;"></iframe>';
}

function loadQuizAttempt() {
  // Load dashboard.html into the content div
  document.getElementById("content").innerHTML = '<iframe src="about.html" frameborder="0" style="width: 100vw; height: 100vh;"></iframe>';
}

