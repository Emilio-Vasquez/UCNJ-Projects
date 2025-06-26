// static/js/script.js

console.log("JavaScript is linked and working!");

// Example: DOM interaction
// All this script does is change the color of the header 2 into blue
document.addEventListener("DOMContentLoaded", function() {
    const header = document.querySelector("h2");
    if (header) {
        header.style.color = "blue";
    }
});
