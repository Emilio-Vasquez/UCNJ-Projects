// static/js/script.js

console.log("JavaScript is linked and working!");

// Example: DOM interaction
document.addEventListener("DOMContentLoaded", function() {
    const header = document.querySelector("h2");
    if (header) {
        header.style.color = "#2c3e50";
    }
});
