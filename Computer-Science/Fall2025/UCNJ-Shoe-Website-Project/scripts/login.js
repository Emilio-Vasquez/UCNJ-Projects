var username
var password
var response
const para = document.createElement("p");
const element = document.getElementById("errorcatcher");
// document.cookie = "domain=" + window.location.hostname
// document.cookie = "path=/"

for (let i = 0; i < document.cookie.split("; ").length; i++) {
    console.log("looping")
    if (document.cookie.split("; ")[i].substring(0,4) == "user") {

    }
    if (document.cookie.split("; ")[i].substring(0,4) == "last") {
        console.log("caught cookie")
        if (document.cookie.split("; ")[i].slice(5) == "passwfail") {
            console.log("caught value")
            response = "Wrong password..."
            para.appendChild(document.createTextNode(response));
            element.appendChild(para);
            document.cookie = "last=" + "none" + ";path=/"
        }
        if (document.cookie.split("; ")[i].slice(5) == "nonefail") {
            console.log("caught value")
            response = "You need to create an account first!"
            para.appendChild(document.createTextNode(response));
            element.appendChild(para);
            document.cookie = "last=" + "none" + ";path=/"
        }
        if (document.cookie.split("; ")[i].slice(5) == "fullfail") {
            console.log("caught value")
            response = "Wrong username/password..."
            para.appendChild(document.createTextNode(response));
            element.appendChild(para);
            document.cookie = "last=" + "none" + ";path=/"
        }
    }

}
console.log(document.cookie)

function login() {
        for (let i = 0; i < document.cookie.split("; ").length; i++) {
            console.log("looping secondary")
            if (document.cookie.split("; ")[i].substring(0,4) == "user") {
                username = document.cookie.split("; ")[i].slice(5)
                console.log("caught username")
            }
            if (document.cookie.split("; ")[i].substring(0,4) == "pass") {
                password = document.cookie.split("; ")[i].slice(5)
                console.log("caught password")
            }
        }
        if (document.getElementById('username').value == username) {
            console.log("username test pass")
            if (document.getElementById('password').value == password) {
                console.log("password test pass")
                document.cookie = "last=" + "pass" + ";path=/"
                window.location.href = window.location.origin;
                }
            else {
                console.log("password test fail")
                document.cookie = "last=" + "passwfail" + ";path=/"
            }
        }
        else if (!username) {
            console.log("username test fail, no account found")
            document.cookie = "last=" + "nonefail" + ";path=/"
        }
        else {
            document.cookie = "last=" + "fullfail" + ";path=/"
        }

}