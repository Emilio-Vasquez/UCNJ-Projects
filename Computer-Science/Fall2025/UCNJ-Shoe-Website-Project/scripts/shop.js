var cartcookie
var pricecookie
var username
var logged
var nameshower = document.getElementById("login")
var cartshower = document.getElementById("cart")
// document.cookie = "domain=" + window.location.hostname
// document.cookie = "path=/"

console.log(document.cookie);
for (let i = 0; i < document.cookie.split("; ").length; i++) {
    if (document.cookie.split("; ")[i].substring(0,4) == "cart") {
        cartcookie = document.cookie.split("; ")[i].slice(5);
    }
    if (document.cookie.split("; ")[i].substring(0,4) == "cpri") {
        pricecookie = document.cookie.split("; ")[i].slice(5);
    }
    if (document.cookie.split("; ")[i].substring(0,4) == "user") {
        username = document.cookie.split("; ")[i].slice(5);
    }
    if (document.cookie.split("; ")[i] == "last=pass") {
        logged = true
    }
}
if (logged){
    nameshower.textContent="Welcome, " + username +"!";
}
cartshower.textContent="Cart (" + String(cartcookie.split(",").length - 1) +")";
function addToCart(ItemName, ItemPrice){
    if (!cartcookie) {
        cartcookie = ItemName + ","
    }
    else {
        cartcookie += ItemName + ",";
    }
    if (!pricecookie) {
        pricecookie = String(ItemPrice) + ","
    }
    else {
        pricecookie += String(ItemPrice) + ",";
    }
    document.cookie = "cart=" + cartcookie + ";path=/";
    document.cookie = "cpri=" + pricecookie + ";path=/";
    cartshower.textContent= "Cart (" + String(cartcookie.split(",").length - 1) +")";
    console.log(cartcookie.split(",").length - 1);
    console.log(document.cookie);
}
