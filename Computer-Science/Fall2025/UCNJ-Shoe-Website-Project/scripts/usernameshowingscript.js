var username
var logged
var cartsize
var carted
var nameshower = document.getElementById("login")
var cartshower = document.getElementById("cart")
// document.cookie = "domain=" + window.location.hostname


console.log('loaded')
console.log(document.cookie)
for (let i = 0; i < document.cookie.split("; ").length; i++) {
    if (document.cookie.split("; ")[i].substring(0,4) == "user") {
        username = document.cookie.split("; ")[i].slice(5);
        console.log('got the user')
    }
    if (document.cookie.split("; ")[i].substring(0,4) == "cart") {
        cartsize = document.cookie.split("; ")[i].split(",").length - 1;
        carted = true
        console.log('got the cart')
    }
    if (document.cookie.split("; ")[i] == "last=pass") {
        console.log('passed')
        logged = true
    }
}
if (carted) {
    console.log('showing cart')
    cartshower.textContent = "Cart (" + String(cartsize) +")";
}
if (logged){
    console.log('showing name')
    nameshower.textContent = "Welcome, " + username +"!";
}